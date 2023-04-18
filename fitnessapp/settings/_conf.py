import pathlib

__all__ = ('BASE_DIR', 'DB_CONFIG', 'API_V',
           'EMAIL_HOST', 'EMAIL_HOST_USER', 'EMAIL_PORT', 'EMAIL_HOST_PASSWORD',
           'PRIVATE_KEY_PATH', 'GOOGLE_CLIENT_ID'
           )

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

DB_CONFIG = {
    'connections': {
        'default': f'sqlite://{BASE_DIR / "db.sqlite"}'
    },
    'apps': {
        'user': {
            'models': [
                'fitnessapp.api.user.models',
                'fitnessapp.web.user.models',
            ],
            'default_connection': 'default',
        }
    },
    'use_tz': True,
    'timezone': 'UTC'
}

API_V = '1.0'

PRIVATE_KEY_PATH = BASE_DIR / 'private_key.pem'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'yuliyasukach123@gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_PASSWORD = 'nwfrmrqvnhjcbmgs'
GOOGLE_CLIENT_ID = '121483820619-lr68ifev2038buns1ite5va1fmibt87i.apps.googleusercontent.com'

