from . import views

def setup_routes(app):
    app.router.add_route('*', '/user/account', views.UserView, name='user_view')
    app.router.add_route('*', '/user/auth', views.AuthView, name='auth_view')
    app.router.add_route('*', '/user/access', views.AccessView, name='access_view')
