import json
import os

import jinja2
from aiohttp import web
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_jinja2 import setup as jinja_setup
from tortoise.contrib.aiohttp import register_tortoise
from fitnessapp.utils.crypto import Enigma
from fitnessapp import settings
from .middles import check_data, check_info, auth_token
from .websocket import websocket_handler
from ..web.user.view.chat import UserChat
from ..web.user.view.diary import AddMeal, UserDiary
from ..web.user.views import UserDetails, UserGoals

from fitnessapp.web.root.urls import setup_routes as root_setup_routes

def create_app():
    app = web.Application(middlewares=(check_data, check_info, auth_token))  # create application

    app['SECRET_KEY'] = os.urandom(32)
    session_setup(app, EncryptedCookieStorage(app['SECRET_KEY']))

    static_dir = settings.BASE_DIR / 'web/user/static'
    dynamic_dir = settings.BASE_DIR / 'web/user/dynamic'

    async def serve_static(request):
        path = request.match_info.get('path', '')
        full_path = static_dir / path.lstrip('/')
        if not full_path.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(full_path)

    async def serve_dynamic(request):
        path = request.match_info.get('path', '')
        full_path = dynamic_dir / path.lstrip('/')
        if not full_path.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(full_path)

    app.router.add_route('GET', '/static/{path:.*}', serve_static)
    app.router.add_route('GET', '/dynamic/{path:.*}', serve_dynamic)
    # Add the WebSocket connection handler
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

    root_setup_routes(app)
    register_tortoise(app, config=settings.DB_CONFIG, generate_schemas=True)

    # Add the route for the Dynamic url
    app.add_routes([web.route('*', '/messages/{recipient_id}', UserChat)])
    app.add_routes([web.route('*', '/profile/{user_id}', UserDetails)])
    app.add_routes([web.route('*', '/account/create/{step_name}', UserGoals)])
    app.add_routes([web.route('DELETE', '/profile/meal', UserDiary)])
    return app


async def get_app():
    return create_app()
