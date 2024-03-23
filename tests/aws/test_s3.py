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

import json
import unittest

import boto3
from moto import mock_aws

from src.aws import s3


class TestGetObjectUrl(unittest.TestCase):
    def test_get_object_url_with_default_region(self):
        self.assertEqual(
            s3.get_object_url("test-bucket", "my-key", "us-east-1"), "https://test-bucket.s3.amazonaws.com/my-key"
        )

    def test_get_object_url_with_non_default_region(self):
        self.assertEqual(
            s3.get_object_url("test-bucket", "my-key", "ap-northeast-1"),
            "https://test-bucket.s3.ap-northeast-1.amazonaws.com/my-key",
        )


@mock_aws
class TestS3Client(unittest.TestCase):
    @mock_aws
    def setUp(self):
        self.bucket = "test-bucket"
        self.key = "test.json"
        self.contents = {"name": "test"}

        # Create a mock S3 bucket and file
        self.s3 = boto3.resource("s3", region_name="us-east-1")
        self.s3.create_bucket(Bucket=self.bucket)

        obj = self.s3.Object(self.bucket, self.key)
        obj.put(Body=json.dumps(self.contents))

        self.client = s3.S3Client(client=self.s3)

    @mock_aws
    def test_put_file(self):
        key = "test.txt"
        contents = "test"
        self.client.put_file(self.bucket, key, contents)

        obj = self.s3.Object(self.bucket, key).get()
        self.assertEqual(obj["Body"].read().decode("utf-8"), contents)

    @mock_aws
    def test_get_file(self):
        response = self.client.get_file(self.bucket, self.key)

        self.assertIn("Body", response)
        self.assertEqual(response["Body"].read().decode("utf-8"), json.dumps(self.contents))

    @mock_aws
    def test_get_json_contents(self):
        response = self.client.get_json_contents(self.bucket, self.key)

        self.assertEqual(response, self.contents)
