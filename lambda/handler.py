import os
from src.decrypt import decrypt_file
from src.s3_utils import list_inbound_files, get_inbound_file, save_outbound_file
import json

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_INBOUND_PREFIX = os.getenv("S3_INBOUND_PREFIX")
S3_OUTBOUND_PREFIX = os.getenv("S3_OUTBOUND_PREFIX")
SECRET_KEY = os.getenv("SECRET_KEY")


def handler(event, context):
    inbound_files = list_inbound_files(S3_BUCKET_NAME, S3_INBOUND_PREFIX)

    for file_name in inbound_files:
        encrypted_data = get_inbound_file(S3_BUCKET_NAME, S3_INBOUND_PREFIX, file_name)
        decrypted_data = decrypt_file(encrypted_data, SECRET_KEY)
        save_outbound_file(S3_BUCKET_NAME, S3_OUTBOUND_PREFIX, file_name, decrypted_data)

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Files processed successfully"})
    }