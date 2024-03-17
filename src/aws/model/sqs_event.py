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

from typing import (
    List,
)

from pydantic import (
    BaseModel,
)


class Attributes(BaseModel):
    ApproximateReceiveCount: str
    SentTimestamp: str
    SenderId: str
    ApproximateFirstReceiveTimestamp: str


class SqsRecord(BaseModel):
    messageId: str
    receiptHandle: str
    body: str
    attributes: Attributes
    md5OfBody: str
    eventSource: str
    eventSourceARN: str
    awsRegion: str


class SqsEvent(BaseModel):
    Records: List[SqsRecord]
