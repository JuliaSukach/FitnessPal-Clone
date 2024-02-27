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
