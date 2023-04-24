from aiohttp import web
connected_clients = []


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    # Add the WebSocket client to the list of connected clients
    connected_clients.append(ws)

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                if msg.data == 'close':
                    await ws.close()
            elif msg.type == web.WSMsgType.ERROR:
                print('ws connection closed with exception %s' % ws.exception())
    finally:
        # Remove the WebSocket client from the list of connected clients
        connected_clients.remove(ws)
        print('websocket connection closed')
    return ws
