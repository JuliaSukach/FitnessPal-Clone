import json
import os

import jwt as jwt
from aiohttp import web
from datetime import datetime, timedelta
from tortoise.exceptions import DoesNotExist
from fitnessapp.utils.crypto import Enigma
from fitnessapp.api.user.models import User
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fitnessapp.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from fitnessapp.utils.crypto import fernet
from fitnessapp.permissions import Admin, Staff, Simple
import base64


class Serializer(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)


class UserView(web.View):
    async def get(self):
        data = await self.request.json()
        user = await User.get(username=data['username']).values('id', 'username', 'email', 'created', 'status')
        return web.json_response({'result': user}, status=200, dumps=lambda v: json.dumps(v, cls=Serializer))

    async def post(self):
        data = await self.request.json()
        new_user = await User.create(**data)
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

        return web.json_response({'result': f'{new_user.username=}'}, status=200)

    async def put(self):
        data = await self.request.json()
        if isinstance(data, dict):
            user = await User.filter(username=data.pop('username')).update(**data)
        elif isinstance(data, list):
            u_name = [el['username'] for el in data]
            users = await User.filter(username__in=u_name)
            for rec, usr in zip(data, users):
                rec.pop('username')
                await usr.update_from_dict(rec)
                await usr.save(update_fields=list(rec.keys()))
        return web.json_response({'result': 'text'}, status=200)

    async def delete(self):
        data = await self.request.json()
        user = await User.get(username=data['username'])
        await user.delete()
        return web.json_response({'result': f'User: {user.id=} was deleted'}, status=200)
        return web.json_response({'result': 'text'}, status=200)


class AccessView(web.View):
    async def post(self):
        data = await self.request.json()
        refresh = data.get('refresh', None)
        try:
            alg = jwt.get_unverified_header(refresh)['alg']
        except jwt.InvalidTokenError:
            return web.json_response({'message': 'Invalid data'}, status=401)
        try:
            payload = jwt.decode(
                refresh, Enigma.public_key, issuer='refresh', algorithms=[alg]
            )
        except jwt.InvalidIssuerError:
            return web.json_response({'message': 'Invalid issuer'}, status=401)
        user = await User.get(username=payload['username'])
        time_stamp = datetime.now()
        if refresh != user.refresh:
            raise web.HTTPNotFound()  # TODO: proccess error
        access_payload = {
            'username': user.username,
            'exp': time_stamp + timedelta(minutes=50),
            'iss': 'access',
            'aud': user.status.name
        }
        access_token = jwt.encode(
            access_payload,
            Enigma.private_key,
            algorithm='RS256',
            headers={'alg': 'RS256'}
        )
        await user.save(update_fields=['refresh'])
        return web.json_response(
            {'access': access_token}, status=201
        )


class AuthView(web.View):
    async def post(self):
        data = await self.request.json()
        try:
            user = await User.get(username=data['username'])
        except DoesNotExist:
            return web.json_response(
                {'message': f'User: {data["username"]} not found'}, status=404
            )
        if await user.check_password(data['password']):
            time_stamp = datetime.now()
            payload = {
                'username': user.username,
                'exp': time_stamp + timedelta(days=5),
                'iss': 'refresh'
            }
            expire = int((time_stamp + timedelta(days=5)).timestamp()) - int(time_stamp.timestamp())
            refresh_token = jwt.encode(
                payload,
                Enigma.private_key,
                algorithm='RS256',
                headers={'alg': 'RS256'}
            )
            user.refresh = refresh_token
            await user.save(update_fields=['refresh'])
            return web.json_response({'refresh': refresh_token, 'expire': expire})
        return web.json_response({'message': f'User: {data["username"]} not found'}, status=404)

    async def delete(self):
        # remove refresh_token
        ...

