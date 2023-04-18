from controller import Controller
from . import views

Controller.add('/register', views.UserAuth, name='user')
