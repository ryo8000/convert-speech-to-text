import json
import unittest

import boto3
from moto import mock_aws

from src.aws import s3


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
