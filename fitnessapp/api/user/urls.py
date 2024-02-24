from controller import Controller
from . import views

Controller.add('/account', views.UserView, name='user_view')
Controller.add('/auth', views.AuthView, name='auth_view')
Controller.add('/access', views.AccessView, name='access_view')
