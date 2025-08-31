from cryptography import fernet
import os


def decrypt_file(encrypted_data: bytes, secret_key: str) -> bytes:
    f = fernet.Fernet(secret_key)
    return f.decrypt(encrypted_data)
