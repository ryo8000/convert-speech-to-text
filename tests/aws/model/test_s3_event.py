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
import os
import unittest

from src.aws.model import S3, Bucket, Identity, S3Event, S3Object, S3Record


class TestS3Event(unittest.TestCase):

    def setUp(self):
        self.s3_event = S3EventFactory.create_s3_event()

    def test_from_event(self):
        s3_event = {}
        event_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "events", "s3-event.json")
        with open(event_file_path) as event_file:
            s3_event = json.load(event_file)

        actual = S3Event.from_event(s3_event)
        self.assertEqual(self.s3_event, actual)

    def test_get_bucket_and_key(self):
        bucket, key = self.s3_event.get_bucket_and_key()
        self.assertEqual(bucket, "my-bucket")
        self.assertEqual(key, "input/audiofile.mp3")


class S3EventFactory:

    @staticmethod
    def create_s3_event() -> S3Event:
        return S3Event(
            records=[
                S3Record(
                    event_version="2.1",
                    event_source="aws:s3",
                    aws_region="us-east-2",
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
