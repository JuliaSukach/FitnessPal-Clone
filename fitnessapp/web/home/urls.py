from aiohttp import web_exceptions
from controller import Controller
from .views import HomePage, AccountPage, ActivateUserView

Controller.add('', HomePage, name='home_page')
Controller.add('/account', AccountPage, name='account_page')
Controller.add('/activate/{user_id}', ActivateUserView, name='activate_user')

