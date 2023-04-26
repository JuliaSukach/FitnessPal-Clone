import json

from fitnessapp.app.websocket import connected_clients


async def broadcast(message, sender, name):
    for ws in connected_clients:
        await ws.send_str(json.dumps({
            'message': message,
            'sender': sender,
            'sender_name': name
        }))
