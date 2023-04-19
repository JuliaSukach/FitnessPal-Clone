import os

import jinja2
import pathlib
from aiohttp import web
from aiohttp_jinja2 import setup as jinja_setup
from tortoise.contrib.aiohttp import register_tortoise
from controller import controller_setup
from fitnessapp.utils.crypto import Enigma
from fitnessapp import settings
from .middles import check_data, check_info, auth_token


def create_app():
    app = web.Application(middlewares=(check_data, check_info, auth_token))  # create application

    static_dir = settings.BASE_DIR / 'web/user/static'

    async def serve_static(request):
        path = request.match_info.get('path', '')
        full_path = static_dir / path.lstrip('/')
        if not full_path.is_file():
            raise web.HTTPNotFound()
        return web.FileResponse(full_path)

    app.router.add_route('GET', '/static/{path:.*}', serve_static)

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
    return app


async def get_app():
    return create_app()
