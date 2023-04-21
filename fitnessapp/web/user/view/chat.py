import json

import aiohttp
from aiohttp import web
from aiohttp_jinja2 import template

from fitnessapp.web.user.models import User, Message


class UserChat(web.View):
    @template('chat.html')
    async def get(self):
        return {'key': 'Info'}

    async def chat_handler(request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        user = request['user']  # get the authenticated user

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                data = json.loads(msg.data)
                recipient = await User.get(id=data['recipient_id'])
                message = Message(sender=user, recipient=recipient, content=data['content'])
                await message.save()
                response_data = {
                    'sender_username': user.username,
                    'recipient_username': recipient.username,
                    'content': message.content,
                    'timestamp': message.timestamp.isoformat(),
                }
                await ws.send_json(response_data)

        return ws
