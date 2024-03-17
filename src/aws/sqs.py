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

"""SQS module."""

import json

from .model import (
    SqsEvent,
)


def convert_sqs_event(data: dict) -> SqsEvent:
    return SqsEvent(**data)


def get_message_info_list(sqs_event: dict) -> list:
    que_info_list = []
    for record in sqs_event["Records"]:
        src_event = json.loads(record["body"])
        que_info_list.append(src_event)
    return que_info_list
