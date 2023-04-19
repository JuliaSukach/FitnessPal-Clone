from controller import Controller
from . import views

Controller.add('/register', views.UserAuth, name='user')
Controller.add('/auth/google/callback', views.GoogleOAuth2Callback, name='google_callback')
