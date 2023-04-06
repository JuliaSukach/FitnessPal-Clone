from aiohttp import web
from .srv import create_app

try:
    web.run_app(create_app(), host='localhost', port=8000)
except KeyboardInterrupt:
    print('\rStop Fitness App')

