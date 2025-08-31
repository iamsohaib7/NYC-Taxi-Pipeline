import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
print(BASE_DIR)
load_dotenv(BASE_DIR / ".env")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
ENCRYPTED_FILES_PATH = os.getenv("ENCRYPTED_FILES_PATH")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_PREFIX = "inbound"

if not all(
    [
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_DEFAULT_REGION,
        ENCRYPTED_FILES_PATH,
        S3_BUCKET_NAME,
    ]
):
    logger.error("Missing required environment variables.")
    raise EnvironmentError(
        "Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, ENCRYPTED_FILES_PATH, S3_BUCKET_NAME are set."
    )

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_DEFAULT_REGION,
)


def upload_file(local_path: Path) -> bool:

    file_name = local_path.name
    s3_key = f"{S3_PREFIX}/{file_name}"
    logger.info(f"Uploading {local_path} → s3://{S3_BUCKET_NAME}/{s3_key}")

    try:
        s3_client.upload_file(str(local_path), S3_BUCKET_NAME, s3_key)
        return True
    except ClientError as e:
        logger.exception(f"AWS error uploading {local_path}: {e}")
    except Exception as e:
        logger.exception(f"Unexpected error for {local_path}: {e}")
    return False


def upload_all():
    base = Path(ENCRYPTED_FILES_PATH)
    files = [p for p in base.rglob("*") if p.is_file()]
    if not files:
        logger.warning("No files found under encrypted path.")
        return
    logger.info(
        f"Found {len(files)} files. Uploading serially..."
    )
    for f in files:
        success = upload_file(f)
        logger.info(f"{f} → {'OK' if success else 'FAIL'}")


if __name__ == "__main__":
    upload_all()
    logger.info("Upload script finished.")
