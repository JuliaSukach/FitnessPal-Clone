from aiohttp import web
from aiohttp_jinja2 import template
from tortoise.exceptions import DoesNotExist

from fitnessapp.api.user.models import User


import base64
from fitnessapp.utils.crypto import fernet


class HomePage(web.View):
    @template('home.html')
    async def get(self):
        return {'key': 'Info'}


class AccountPage(web.View):
    @template('home.html')
    async def get(self):
        return {'key': 'Info'}

class ActivateUserView(web.View):
    async def get(self):
        encoded_link = self.request.match_info['user_id']
        try:
            encrypted_link = base64.urlsafe_b64decode(encoded_link.encode()).decode()
            link = fernet.decrypt(encrypted_link.encode()).decode()
            user_id = link.split('/')[-1]
            user = await User.get(id=user_id)
            if user.is_active:
                return web.json_response({'message': 'User is already activated'}, status=400)

            user.is_active = True
            await user.save(update_fields=['is_active'])
        except DoesNotExist:
            return web.json_response({'message': f'User with id {user_id} does not exist.'}, status=404)
        except Exception as e:
            return web.json_response({'message': str(e)}, status=500)

        # Return a response to the client
        return web.Response(text='Your account has been activated!')
