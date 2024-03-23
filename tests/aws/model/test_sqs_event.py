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

from src.aws.model import SqsEvent, SqsRecord

from .test_s3_event import S3EventFactory


class TestSqsEvent(unittest.TestCase):

    def test_from_event(self):
        sqs_event = {}
        event_file_path = os.path.join(os.path.dirname(__file__), "..", "..", "events", "sqs-event.json")
        with open(event_file_path) as event_file:
            sqs_event = json.load(event_file)

        actual = SqsEvent.from_event(sqs_event)
        self.assertEqual(SqsEventFactory.create_sqs_event(), actual)


class SqsEventFactory:

    @staticmethod
    def create_sqs_event() -> SqsEvent:
        return SqsEvent(
            records=[
                SqsRecord(
                    messageId="059f36b4-87a3-44ab-83d2-661975830a7d",
                    body=S3EventFactory.create_s3_event(),  # normal event
                ),
                SqsRecord(
                    messageId="2e1424d4-f796-459a-8184-9c92662be6da",
                    body=None,  # abnormal event
                ),
            ]
        )
