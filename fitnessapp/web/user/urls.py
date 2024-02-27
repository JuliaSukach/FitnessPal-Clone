# from controller import Controller
# from . import views
# from .view.chat import UserMessenger
# from .view.diary import UserDiary, SearchMeal, AddMeal
# from .view.edit_photo import EditPhoto
#
# Controller.add('/register', views.UserAuth, name='user')
# Controller.add('/login', views.UserLogin, name='user_login')
# Controller.add('/messages', UserMessenger, name='user_messages')
# Controller.add('/profile', views.UserProfile, name='user_profile')
# Controller.add('/food/diary', UserDiary, name='user_diary')
# Controller.add('/food/search', SearchMeal, name='search_meal')
# Controller.add('/auth/google/callback', views.GoogleOAuth2Callback, name='google_callback')
# Controller.add('/food/add_to_diary', AddMeal, name='add_meal')
# Controller.add('/photos/edit', EditPhoto, name='edit_photo')

from . import views
from .view.chat import UserMessenger
from .view.diary import UserDiary, SearchMeal, AddMeal
from .view.edit_photo import EditPhoto

def setup_routes(app):
    app.router.add_route('*', '/user/register', views.UserAuth, name='user')
    app.router.add_route('*', '/user/login', views.UserLogin, name='user_login')
    app.router.add_route('*', '/user/messages', UserMessenger, name='user_messages')
    app.router.add_route('*', '/user/profile', views.UserProfile, name='user_profile')
    app.router.add_route('*', '/user/food/diary', UserDiary, name='user_diary')
    app.router.add_route('*', '/user/food/search', SearchMeal, name='search_meal')
    app.router.add_route('*', '/user/auth/google/callback', views.GoogleOAuth2Callback, name='google_callback')
    app.router.add_route('*', '/user/food/add_to_diary', AddMeal, name='add_meal')
    app.router.add_route('*', '/user/photos/edit', EditPhoto, name='edit_photo')
