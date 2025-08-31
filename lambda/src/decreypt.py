from cryptography import fernet
import os

SECRET_KEY = os.getenv("SECRET_KEY")

def decrypt_file(encrypted_data: bytes) -> bytes:
    f = fernet.Fernet(SECRET_KEY)
    return f.decrypt(encrypted_data)
