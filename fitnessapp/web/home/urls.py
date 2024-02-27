from aiohttp import web_exceptions
from controller import Controller
from .views import HomePage, AccountPage, ActivateUserView

# Controller.add('', HomePage, name='home_page')
# Controller.add('/account', AccountPage, name='account_page')
# Controller.add('/activate/{user_id}', ActivateUserView, name='activate_user')
from .views import HomePage, AccountPage, ActivateUserView


def setup_routes(app):
    app.router.add_get('/', HomePage, name='home_page')
    app.router.add_get('/account', AccountPage, name='account_page')
    app.router.add_get('/activate/{user_id}', ActivateUserView, name='activate_user')
