import os

from dotenv import load_dotenv

from fitnessapp import settings
from fitnessapp.utils.crypto import Enigma

load_dotenv()

if __name__ == '__main__':
    key_pass = os.getenv('KEY_PASS')
    # key_pass = 17101997
    with open(settings.PRIVATE_KEY_PATH, 'w') as key_file:
        key_file.write(Enigma.create_key(2048, key_pass))
