from aiohttp import web
from aiohttp_jinja2 import template

from fitnessapp.utils.myfitnesspal_api import search_food
from fitnessapp.web.user.models import User
from fitnessapp.web.user.views import BaseView


class EditPhoto(BaseView):
    @template('edit_photo.html')
    async def get(self):
        user_id = await self.get_current_user()
        if not user_id:
            return web.HTTPFound(location='/register')
        user = await User.get(id=user_id)

        return {
            'user': user,
            'current_url': str(self.request.rel_url)
        }



