# from controller import Controller
# from fitnessapp.settings import API_V
#
#
# Controller.include('', 'fitnessapp.web.home.urls')
# Controller.include('', 'fitnessapp.web.user.urls')
# Controller.include(f'/api/v_{API_V}', 'fitnessapp.api.root.urls')
from fitnessapp.web.user.urls import setup_routes as user_setup_routes
from fitnessapp.api.root.urls import setup_routes as api_root_setup_routes
from fitnessapp.web.home.urls import setup_routes as home_setup_routes


def setup_routes(app):
    user_setup_routes(app)
    home_setup_routes(app)
    api_root_setup_routes(app)


