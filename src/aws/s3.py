import json
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
    key = urllib.parse.unquote_plus(s3_event["Records"][0]["s3"]["object"]["key"], encoding="utf-8")
    return bucket, key


def get_object_url(bucket: str, key: str, region: str) -> str:
    """Get the url of the S3 object.

    Args:
        bucket: S3 bucket name
        key: S3 key name
        region: S3 bucket region

    Returns:
        the url of the S3 object
    """
    bucket_region = f"{region}." if region != "us-east-1" else ""
    return f"https://{bucket}.s3.{bucket_region}amazonaws.com/{key}"


def get_json_contents(bucket: str, path: str) -> dict:
    response = get_file(bucket, path)
    return json.loads(response["Body"].read().decode("utf-8"))


def get_file(bucket: str, path: str) -> dict:
    return s3.Object(bucket, path).get()


def put_file(bucket: str, path: str, contents: str) -> dict:
    return s3.Object(bucket, path).put(Body=contents)
