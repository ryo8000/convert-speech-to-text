import urllib.parse

import boto3

s3 = boto3.resource("s3")


def get_bucket_path(s3_event: dict) -> tuple:
    """Get S3 bucket name and key from S3 event.

    Args:
        s3_event: S3 event

    Returns:
        S3 bucket name and key
    """
    bucket = s3_event["Records"][0]["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        s3_event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    return bucket, key
