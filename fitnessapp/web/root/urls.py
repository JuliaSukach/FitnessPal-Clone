from fitnessapp.web.user.urls import setup_routes as user_setup_routes
from fitnessapp.api.root.urls import setup_routes as api_root_setup_routes
from fitnessapp.web.home.urls import setup_routes as home_setup_routes


def setup_routes(app):
    user_setup_routes(app)
    home_setup_routes(app)
    api_root_setup_routes(app)


