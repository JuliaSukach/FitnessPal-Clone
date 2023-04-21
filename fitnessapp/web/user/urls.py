from controller import Controller
from . import views
from .view.chat import UserChat

Controller.add('/register', views.UserAuth, name='user')
Controller.add('/login', views.UserLogin, name='user_login')
Controller.add('/messages', UserChat, name='user_messages')
Controller.add('/profile', views.UserProfile, name='user_profile')
Controller.add('/auth/google/callback', views.GoogleOAuth2Callback, name='google_callback')
