import json
from aiohttp import web
from aiohttp.web_response import json_response
from aiohttp_jinja2 import template
from tortoise.expressions import Q

from fitnessapp.utils.broadcast import broadcast
from fitnessapp.utils.serializer import Serializer
from fitnessapp.web.user.models import Message, User
from fitnessapp.web.user.views import BaseView


class UserMessenger(BaseView):
    @template('messenger.html')
    async def get(self):
        sender_id = await self.get_current_user()
        users = await User.all().filter(~Q(id=sender_id))

        return {'recipients': users}

    async def save_message(self, sender, recipient, content):
        print('save message')
        # message = Message(sender=sender, recipient=recipient, content=content)
        # await message.save()

    async def post(self):
        form = await self.request.post()
        message_content = form['message']
        sender_id = await self.get_current_user()
        recipient_id = form['recipient_id']
        await self.save_message(sender_id, recipient_id, message_content)
        return web.HTTPFound('/messages')


class UserChat(BaseView):
    @template('chat.html')
    async def get(self):
        sender_id = await self.get_current_user()
        users = await User.all().filter(~Q(id=sender_id))

        recipient_id = self.request.match_info['recipient_id']
        recipient = await User.get_or_none(id=recipient_id)
        messages = await Message.filter(
                    Q(sender_id=sender_id, recipient_id=recipient_id) |
                    Q(sender_id=recipient_id, recipient_id=sender_id)
                ).order_by('created_at')

        # Add is_sender flag to messages
        for message in messages:
            message.is_sender = message.sender_id == sender_id

        if not recipient:
            raise web.HTTPNotFound()

        return {'recipients': users, 'recipient': recipient, 'messages': messages}

    async def post(self):
        form = await self.request.post()
        recipient_id = form.get('recipient_id')
        message_content = form.get('message')
        sender_id = await self.get_current_user()
        sender = await User.get(id=sender_id)

        # save the message to the database
        await Message.create(sender_id=sender_id, recipient_id=recipient_id, content=message_content)

        await broadcast(message_content, sender_id, sender.username)

        # get the updated chat data
        messages = await Message.filter(
                    Q(sender_id=sender_id, recipient_id=recipient_id) |
                    Q(sender_id=recipient_id, recipient_id=sender_id)
                ).order_by('created_at')

        users = await User.filter(~Q(id=sender_id))
        recipient = await User.get_or_none(id=recipient_id)

        # Add is_sender flag to messages
        for message in messages:
            message.is_sender = message.sender_id == sender_id

        return json_response({'recipients': users, 'recipient': recipient, 'messages': messages}, status=200, dumps=lambda v: json.dumps(v, cls=Serializer))

