import argparse
import logging
import os
from pathlib import Path

from cryptography.fernet import Fernet
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables.")


def encrypt_file(file_path: str) -> None:
    fernet = Fernet(SECRET_KEY.encode())
    with open(file_path, "rb") as file:
        original_data = file.read()
    encrypted_data = fernet.encrypt(original_data)
    with open(file_path, "wb") as file:
        file.write(encrypted_data)


def decrypt_file(file_path: str) -> None:
    fernet = Fernet(SECRET_KEY.encode())
    with open(file_path, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_path, "wb") as file:
        file.write(decrypted_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Encrypt or decrypt a file using Fernet symmetric encryption."
    )
    parser.add_argument(
        "action", choices=["encrypt", "decrypt"], help="Action to perform on the file."
    )
    parser.add_argument(
        "file_path", type=str, help="Path to the file to be encrypted or decrypted."
    )

    args = parser.parse_args()

    if args.action == "encrypt":
        encrypt_file(args.file_path)
        logger.info(f"File '{args.file_path}' has been encrypted.")
    elif args.action == "decrypt":
        decrypt_file(args.file_path)
        logger.info(f"File '{args.file_path}' has been decrypted.")
