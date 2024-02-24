import jwt
import datetime
from fitnessapp.utils.crypto import Enigma


def generate_access_token(user_id):
    payload = {
        'sub': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
        'iat': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, Enigma.private_key, algorithm='RS256',)


def generate_refresh_token(user_id):
    payload = {
        'sub': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, Enigma.private_key, algorithm='RS256')