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
        user = await User.get(username=data['username']).values('id', 'username', 'email', 'created', 'status')
        return web.json_response({'result': user}, status=200, dumps=lambda v: json.dumps(v, cls=Serializer))

    async def post(self):
        data = await self.request.json()
        new_user = await User.create(**data)
        return web.json_response({'result': f'{new_user.id=}'}, status=200)

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
