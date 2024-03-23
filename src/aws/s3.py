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
