import json
import os
import unittest

from src.aws.model import S3, Bucket, Identity, S3Event, S3Object, S3Record


class TestS3Event(unittest.TestCase):

    def setUp(self):
        self.s3_event = S3EventFactory.create_s3_event()

    def test_from_event(self):
        contents = {}
        file_path = os.path.join(os.path.dirname(__file__), "..", "..", "events", "s3-event.json")
        with open(file_path) as file:
            contents = json.load(file)

        s3_event = S3Event.from_event(contents)
        self.assertEqual(s3_event, self.s3_event)

    def test_get_bucket_and_key(self):
        bucket, key = self.s3_event.get_bucket_and_key()
        self.assertEqual(bucket, "my-bucket")
        self.assertEqual(key, "input/audiofile.mp3")

    def test_get_object_url_with_default_region(self):
        s3_event = S3EventFactory.create_s3_event("us-east-1")
        self.assertEqual(
            s3_event.get_object_url(),
            "https://my-bucket.s3.amazonaws.com/input/audiofile.mp3",
        )

    def test_get_object_url_with_non_default_region(self):
        self.assertEqual(
            self.s3_event.get_object_url(),
            "https://my-bucket.s3.us-east-2.amazonaws.com/input/audiofile.mp3",
        )


class S3EventFactory:

    @staticmethod
    def create_s3_event(region: str = "us-east-2") -> S3Event:
        return S3Event(
            records=[
                S3Record(
                    event_version="2.1",
                    event_source="aws:s3",
                    aws_region=region,
                    event_time="2019-09-03T19:37:27.192Z",
                    event_name="ObjectCreated:Put",
                    user_identity=Identity(principal_id="AWS:AIDAINPONIXQXHT3IKHL2"),
                    s3=S3(
                        s3_schema_version="1.0",
                        configuration_id="MyEvent",
                        bucket=Bucket(
                            name="my-bucket",
                            owner_identity=Identity(principal_id="A3I5XTEXAMAI3E"),
                            arn="arn:aws:s3:::my-bucket",
                        ),
                        object=S3Object(
                            key="input/audiofile.mp3",
                            size=1305107,
                            e_tag="b21b84d653bb07b05b1e6b33684dc11b",
                            sequencer="0C0F6F405D6ED209E1",
                        ),
                    ),
                )
            ]
        )
