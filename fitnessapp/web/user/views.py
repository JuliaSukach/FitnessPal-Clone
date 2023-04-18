import base64
import json
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiohttp import web
from aiohttp_jinja2 import template

from fitnessapp.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

from .models import User
# from fitnessapp.api.user.models import User
from ...utils.crypto import fernet


class UserAuth(web.View):
    @template('register.html')
    async def get(self):
        return {'key': 'Info'}

    async def post(self):
        print(await self.request.text())
        data = await self.request.post()
        # new_user = await User.create(**data)
        new_user = await User.create(username=data['username'], email=data['email'], password=data['password'])
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


