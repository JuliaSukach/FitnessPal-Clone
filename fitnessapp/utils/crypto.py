from cryptography.fernet import Fernet

# generate a secret key for encrypting the link
key = Fernet.generate_key()

fernet = Fernet(key)