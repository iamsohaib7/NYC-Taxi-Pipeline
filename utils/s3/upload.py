import boto3
from botocore.exceptions import ClientError
from pathlib import Path
from dotenv import load_dotenv
import logging, os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
ENCRYPTED_FILES_PATH = os.getenv("ENCRYPTED_FILES_PATH")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, ENCRYPTED_FILES_PATH, S3_BUCKET_NAME]):
    logger.error("Missing required environment variables.")
    raise EnvironmentError("Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, ENCRYPTED_FILES_PATH, S3_BUCKET_NAME are set.")
