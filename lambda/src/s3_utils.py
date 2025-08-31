import boto3
from typing import List


def list_inbound_files(s3_bucket_name: str, s3_inbound_prefix: str) -> List[str]:
    s3_client = boto3.client("s3")
    response = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=s3_inbound_prefix + "/")
    return [obj.get("Key") for obj in response.get("Contents", [])]

def get_inbound_file(s3_bucket_name: str, s3_inbound_prefix: str, file_name: str) -> bytes:
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=s3_bucket_name, Key=f"{s3_inbound_prefix}/{file_name}")
    return response["Body"].read()

def save_outbound_file(s3_bucket_name: str, s3_outbound_prefix: str, file_name: str, data: bytes) -> None:
    s3_client = boto3.client("s3")
    s3_client.put_object(Bucket=s3_bucket_name, Key=f"{s3_outbound_prefix}/{file_name}", Body=data)
