from aiohttp import web_exceptions
from controller import Controller
from .views import HomePage, AccountPage

Controller.add('', HomePage, name='home_page')
Controller.add('/account', AccountPage, name='account_page')

