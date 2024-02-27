from aiohttp import web
from .srv import create_app
import os

try:
    web.run_app(create_app(), host='0.0.0.0', port=os.getenv('PORT'))
except KeyboardInterrupt:
    print('\rStop Fitness App')

