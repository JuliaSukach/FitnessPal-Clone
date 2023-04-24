import json
import os

import jinja2
from aiohttp import web
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_jinja2 import setup as jinja_setup
from tortoise.contrib.aiohttp import register_tortoise
from controller import controller_setup
from fitnessapp.utils.crypto import Enigma
from fitnessapp import settings
from .middles import check_data, check_info, auth_token
from .websocket import websocket_handler
from ..web.user.view.chat import UserChat


def create_app():
    app = web.Application(middlewares=(check_data, check_info, auth_token))  # create application

    app['SECRET_KEY'] = os.urandom(32)
    session_setup(app, EncryptedCookieStorage(app['SECRET_KEY']))

    static_dir = settings.BASE_DIR / 'web/user/static'

    async def serve_static(request):
        path = request.match_info.get('path', '')
        full_path = static_dir / path.lstrip('/')
        if not full_path.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(full_path)

    app.router.add_route('GET', '/static/{path:.*}', serve_static)
    # Add the WebSocket connection handler
    app['websockets'] = []
    app.add_routes([web.get('/ws', websocket_handler)])

    jinja_setup(
        app,
        loader=jinja2.FileSystemLoader(
            [
                path / 'templates'
                for path in (settings.BASE_DIR / 'web').iterdir()
                if path.is_dir() and (path / 'templates').exists()
            ]
        )
    )
    Enigma.load_key(settings.PRIVATE_KEY_PATH)

    controller_setup(app, root_urls='fitnessapp.web.root.urls')  # entry point
    register_tortoise(app, config=settings.DB_CONFIG, generate_schemas=True)

    # Add the route for the Dynamic url
    app.add_routes([web.route('*', '/messages/{recipient_id}',  UserChat)])
    return app


async def get_app():
    return create_app()
