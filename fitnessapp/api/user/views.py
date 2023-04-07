import json
from aiohttp import web
from tortoise.exceptions import DoesNotExist
from datetime import datetime
from fitnessapp.api.user.models import User


class Serializer(json.JSONEncoder):
    def default(self, value):
        if isinstance(value, datetime):
            return value.isoformat()
        return str(value)


class UserView(web.View):
    async def get(self):
        data = await self.request.json()
        user = await User.get(username=data['username']).values()
        return web.json_response({'result': user}, status=200, dumps=lambda v: json.dumps(v, cls=Serializer))

    async def post(self):
        data = await self.request.json()
        new_user = await User.create(**data)
        return web.json_response({'result': f'{new_user.id=}'}, status=200)

    async def put(self):
        data = await self.request.json()
        return web.json_response({'result': 'text'}, status=200)

    async def delete(self):
        data = await self.request.json()
        return web.json_response({'result': 'text'}, status=200)