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

"""SQS event module."""

import json
from dataclasses import (
    dataclass,
)
from typing import (
    List,
    Optional,
)

from .s3_event import (
    S3Event,
)


@dataclass
class SqsRecord:
    messageId: str
    body: Optional[S3Event]

    @classmethod
    def from_event(cls, event: dict):
        body_dict = json.loads(event["body"])
        # when s3 event is a test event, the key of "Records" is not present
        s3_event = S3Event.from_event(body_dict) if body_dict.get("Records", {}) else None
        return cls(
            messageId=event["messageId"],
            body=s3_event,
        )


@dataclass
class SqsEvent:
    records: List[SqsRecord]

    @classmethod
    def from_event(cls, event: dict):
        return cls([SqsRecord.from_event(r) for r in event["Records"]])
