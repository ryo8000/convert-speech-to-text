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

from src.aws import (
    lambda_event,
)

from .model.s3_event import (
    S3EventFactory,
)
from .model.sqs_event import (
    SqsEventFactory,
)


class TestConvertDictToSqsEvent(unittest.TestCase):
    def test_convert_dict_to_sqs_event_normal(self):
        sqs_event = {}
        event_file_path = os.path.join(os.path.dirname(__file__), "..", "events", "sqs-event-normal.json")
        with open(event_file_path) as event_file:
            sqs_event = lambda_event.convert_dict_to_sqs_event(json.load(event_file))

        s3_event = S3EventFactory.create_s3_event()
        self.assertEqual(sqs_event, SqsEventFactory.create_sqs_event(s3_event))

    def test_convert_dict_to_sqs_event_abnormal(self):
        sqs_event = {}
        event_file_path = os.path.join(os.path.dirname(__file__), "..", "events", "sqs-event-abnormal.json")
        with open(event_file_path) as event_file:
            sqs_event = lambda_event.convert_dict_to_sqs_event(json.load(event_file))

        s3_event = None
        self.assertEqual(sqs_event, SqsEventFactory.create_sqs_event(s3_event))
