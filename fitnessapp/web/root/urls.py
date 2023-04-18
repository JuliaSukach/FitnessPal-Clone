from controller import Controller
from fitnessapp.settings import API_V


Controller.include('', 'fitnessapp.web.home.urls')
Controller.include('', 'fitnessapp.web.user.urls')
Controller.include(f'/api/v_{API_V}', 'fitnessapp.api.root.urls')

