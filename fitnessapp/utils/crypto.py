import os
import base64
from typing import Union

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.types import PRIVATE_KEY_TYPES, PUBLIC_KEY_TYPES
from dotenv import load_dotenv


class Enigma:
    private_key: PRIVATE_KEY_TYPES = None
    public_key: PUBLIC_KEY_TYPES = None

    @staticmethod
    def create_key(key_size: int, passphrase: str):
        _private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        return _private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(passphrase.encode('utf-8'))
        ).decode('utf-8')

    @classmethod
    def load_key(cls, path):
        load_dotenv()
        with open(path, mode='rb') as _key_file:
            cls.private_key = serialization.load_pem_private_key(
                _key_file.read(), password=os.getenv('KEY_PASS_STR').encode('utf-8')
            )
            cls.public_key = cls.private_key.public_key()

    @classmethod
    def encrypt(cls, value: Union[str, bytes]) -> Union[str, bytes]:
        data = cls.public_key.encrypt(
            value.encode('utf-8') if isinstance(value, str) else value,
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()), algorithm=hashes.SHA512(), label=None)
        )
        return base64.b64encode(data).decode('utf-8') if isinstance(value, str) else data

    @classmethod
    def decrypt(cls, value: Union[str, bytes]) -> Union[str, bytes]:
        data = cls.private_key.decrypt(
            base64.b64decode(value) if isinstance(value, str) else value,
            padding=padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA512()), algorithm=hashes.SHA512(), label=None)
        )
        return data.decode('utf-8') if isinstance(value, str) else data


if __name__ == '__main__':
    import pathlib
    from fitnessapp import settings
    os.environ['KEY_PASS'] = '17101997'

    # test preparation
    private_key_path = pathlib.Path(__file__).parent.absolute() / 'tmp_key.pem'
    with open(private_key_path, 'w') as key_file:
        key_file.write(Enigma.create_key(2048, os.getenv('KEY_PASS')))

    Enigma.load_key(private_key_path)

    # test
    info = 'text'
    res = Enigma.encrypt(info)
    assert Enigma.decrypt(res) == info


# generate a secret key for encrypting the link
key = Fernet.generate_key()

fernet = Fernet(key)
