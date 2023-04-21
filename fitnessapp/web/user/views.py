import base64
import smtplib
import ssl
from typing import Optional
import jwt

import arrow
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiohttp
from aiohttp import web
from aiohttp_jinja2 import template
from aiohttp_session import get_session

from fitnessapp.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, GOOGLE_CLIENT_ID, \
    GOOGLE_CLIENT_SECRET
from .models import User, Post, Comment
from ...utils.crypto import fernet, Enigma
from ...utils.tokens import generate_access_token, generate_refresh_token


class UserProfile(web.View):
    async def get_current_user(self) -> Optional[User]:
        refresh = self.request.cookies.get('refresh_token')
        try:
            alg = jwt.get_unverified_header(refresh)['alg']
        except jwt.InvalidTokenError:
            return web.json_response({'message': 'Invalid data'}, status=401)
        try:
            payload = jwt.decode(refresh, Enigma.public_key, algorithms=[alg])
        except jwt.exceptions.InvalidTokenError:
            return None
        user_id = payload.get('sub')
        if not user_id:
            return None
        user = await User.get(id=user_id)
        return user
        # # return await User.get(username='yuliyasukach123@gmail.com')

    @template('profile.html')
    async def get(self):
        user = await self.get_current_user()
        if not user:
            return web.HTTPFound(location='/register')
        posts = await Post.all().order_by('-created_at').select_related('user')
        posts_dict = {}
        comments_dict = {}
        for post in posts:
            comments = await post.comments.all().select_related('user')
            comments_data = []
            for comment in comments:
                # calculate time ago for comment
                created_at = arrow.get(comment.created_at).humanize()
                comments_data.append({
                    'id': comment.id,
                    'content': comment,
                    'username': comment.user.username,
                    'created_at': created_at
                })
            comments_dict[post.id] = comments_data
            posts_dict[post.id] = {
                'post': post,
                'comments': comments_data,
                'username': post.user.username,
                'created_at': arrow.get(post.created_at).humanize()
            }
        return {'posts': posts_dict, 'user': user}

    async def post(self):
        if 'create_post' in await self.request.post():
            user = await self.get_current_user()
            post_data = await self.request.post()
            content = post_data.get('content')
            await Post.create(user=user, content=content)
            return web.HTTPFound(location='/profile')
        elif 'create_comment' in await self.request.post():
            user = await self.get_current_user()
            comment_data = await self.request.post()
            post_id = int(comment_data.get('post_id'))
            content = comment_data.get('create_comment')
            post = await Post.get(id=post_id)
            await Comment.create(user=user, post=post, content=content)
            return web.HTTPFound(location='/profile')
        elif 'delete_comment_id' in await self.request.post():
            comment_data = await self.request.post()
            comment_id = int(comment_data.get('delete_comment_id'))
            await self.delete_comment(comment_id)
            return web.HTTPFound(location='/profile')
        elif 'delete_post' in await self.request.post():
            post_data = await self.request.post()
            post_id = int(post_data.get('delete_post'))
            await self.delete_post(post_id)
            return web.HTTPFound(location='/profile')
        elif 'logout' in await self.request.post():
            response = web.HTTPFound('/login')
            response.del_cookie('access_token')
            response.del_cookie('refresh_token')
            return response
        else:
            pass

    async def delete_comment(self, comment_id):
        comment = await Comment.get(id=comment_id)
        await comment.delete()

    async def delete_post(self, post_id):
        post = await Post.get(id=post_id)
        await post.delete()


class UserAuth(web.View):
    @template('register.html')
    async def get(self):
        return {'key': 'Info'}

    async def post(self):
        data = await self.request.post()
        new_user = await User.create(username=data['username'], email=data['email'], password=data['password'])

        # create and save session
        session = await get_session(self.request)
        session['user_id'] = new_user.id

        # generate access and refresh tokens
        access_token = generate_access_token(new_user.id)
        refresh_token = generate_refresh_token(new_user.id)

        new_user.refresh = refresh_token
        await new_user.save(update_fields=['refresh'])

        # Set cookies for tokens in the response
        response = web.HTTPFound('/profile')
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True)

        context = ssl.create_default_context()

        # send email to new user
        msg = MIMEMultipart()
        msg['Subject'] = 'Welcome to My Website!'
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = new_user.email

        # create message body
        link = f"http://localhost:8000/activate/{new_user.id}"
        encrypted_link = fernet.encrypt(link.encode()).decode()
        encoded_link = base64.urlsafe_b64encode(encrypted_link.encode()).decode()

        final_link = f"http://localhost:8000/activate/{encoded_link}"
        body = f"Dear {new_user.username},\n\nWelcome to My Website!" \
               f"Thank you for creating an account." \
               f"Please click on the following link to activate your account: {final_link}"

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls(context=context)
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

            server.sendmail(EMAIL_HOST_USER, new_user.email, msg.as_string())
        except Exception as e:
            print(e)
        finally:
            server.quit()

        return response


class UserLogin(web.View):
    @template('login.html')
    async def get(self):
        return {'key': 'Info'}

    async def post(self):
        data = await self.request.post()

        # check if user exists in the database
        user = await User.get_or_none(username=data['username'])
        if user is None:
            # user not found, return error message
            return web.Response(text="Invalid username or password", status=401)

        # check if password is correct
        if not user.check_password(data['password']):
            # password is incorrect, return error message
            return web.Response(text="Invalid username or password", status=401)

        # set session and tokens for authenticated user
        session = await get_session(self.request)
        session['user_id'] = user.id

        access_token = generate_access_token(user.id)
        refresh_token = generate_refresh_token(user.id)

        user.refresh = refresh_token
        await user.save(update_fields=['refresh'])

        # Set cookies for tokens in the response
        response = web.HTTPFound('/profile')
        response.set_cookie('access_token', access_token, httponly=True)
        response.set_cookie('refresh_token', refresh_token, httponly=True)

        return response


class GoogleOAuth2Callback(web.View):
    async def get(self):
        # Get the authorization code from the query parameters
        authorization_code = self.request.query.get('code')

        # Exchange the authorization code for an access token
        async with aiohttp.ClientSession() as session:
            token_url = 'https://oauth2.googleapis.com/token'
            data = {
                'code': authorization_code,
                'client_id': GOOGLE_CLIENT_ID,
                'client_secret': GOOGLE_CLIENT_SECRET,
                'redirect_uri': 'http://localhost:8000/auth/google/callback',
                'grant_type': 'authorization_code'
            }
            async with session.post(token_url, data=data) as response:
                token_data = await response.json()

                email_url = 'https://www.googleapis.com/oauth2/v1/userinfo?alt=json'
                headers = {
                    'Authorization': f'Bearer {token_data["access_token"]}'
                }
                async with session.get(email_url, headers=headers) as response:
                    email_data = await response.json()

        # Save the user's email address to the database
        email = email_data['email']
        print(email)

        new_user = await User.create(username=email, email=email, password='admin')
        context = ssl.create_default_context()

        # send email to new user
        msg = MIMEMultipart()
        msg['Subject'] = 'Welcome to My Website!'
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = new_user.email

        # create message body
        link = f"http://localhost:8000/activate/{new_user.id}"
        encrypted_link = fernet.encrypt(link.encode()).decode()
        encoded_link = base64.urlsafe_b64encode(encrypted_link.encode()).decode()

        final_link = f"http://localhost:8000/activate/{encoded_link}"
        body = f"Dear {new_user.username},\n\nWelcome to My Website!" \
               f"Thank you for creating an account." \
               f"Please click on the following link to activate your account: {final_link}"

        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls(context=context)
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

            server.sendmail(EMAIL_HOST_USER, new_user.email, msg.as_string())
        except Exception as e:
            print(e)
        finally:
            server.quit()

        return web.HTTPFound('/profile')