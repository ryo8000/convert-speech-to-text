# Copyright 2024 Ryo H
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""S3 module."""

import json
import urllib.parse

import boto3


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
