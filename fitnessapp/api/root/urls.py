# from controller import Controller
#
# Controller.include('/user', 'fitnessapp.api.user.urls')

# from api.user.urls import setup_routes as user_setup_routes
from fitnessapp.api.user.urls import setup_routes as user_setup_routes


def setup_routes(app):
    user_setup_routes(app)
