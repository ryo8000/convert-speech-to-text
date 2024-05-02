"""S3 module."""

import json

import boto3


class S3Client:
    """S3 client class."""

    def __init__(self, client=None):
        """__init__ method.

        Args:
            client (optional): _s3 client.
        """
        self.client = client or boto3.resource("s3")

    def get_json_contents(self, bucket: str, key: str) -> dict:
        """Retrieve the contents of the JSON file in S3.

        Args:
            bucket: S3 bucket name
            key: S3 key name

        Returns:
            dict: result of get file
        """
        response = self.get_file(bucket, key)
        return json.loads(response["Body"].read().decode("utf-8"))

    def get_file(self, bucket: str, key: str) -> dict:
        """Retrieve file in S3.

        Args:
            bucket: S3 bucket name
            key: S3 key name

        Returns:
            dict: result of get file
        """
        return self.client.Object(bucket, key).get()

    def put_file(self, bucket: str, key: str, contents: str) -> dict:
        """Put file to S3.

        Args:
            bucket: S3 bucket name
            key: S3 key name
            contents: file contents

        Returns:
            dict: result of put file
        """
        return self.client.Object(bucket, key).put(Body=contents)
