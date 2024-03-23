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

"""S3 event module."""

import urllib.parse
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Identity:
    principal_id: str

    @classmethod
    def from_event(cls, event: dict):
        return cls(principal_id=event["principalId"])


@dataclass
class Bucket:
    name: str
    owner_identity: Identity
    arn: str

    @classmethod
    def from_event(cls, event: dict):
        return cls(name=event["name"], owner_identity=Identity.from_event(event["ownerIdentity"]), arn=event["arn"])


@dataclass
class S3Object:
    key: str
    size: int
    e_tag: str
    sequencer: str

    @classmethod
    def from_event(cls, event: dict):
        return cls(
            key=urllib.parse.unquote_plus(event["key"], encoding="utf-8"),
            size=event["size"],
            e_tag=event["eTag"],
            sequencer=event["sequencer"],
        )


@dataclass
class S3:
    s3_schema_version: str
    configuration_id: str
    bucket: Bucket
    object: S3Object

    @classmethod
    def from_event(cls, event: dict):
        return cls(
            s3_schema_version=event["s3SchemaVersion"],
            configuration_id=event["configurationId"],
            bucket=Bucket.from_event(event["bucket"]),
            object=S3Object.from_event(event["object"]),
        )


@dataclass
class S3Record:
    event_version: str
    event_source: str
    aws_region: str
    event_time: str
    event_name: str
    user_identity: Identity
    s3: S3

    @classmethod
    def from_event(cls, event: dict):
        return cls(
            event_version=event["eventVersion"],
            event_source=event["eventSource"],
            aws_region=event["awsRegion"],
            event_time=event["eventTime"],
            event_name=event["eventName"],
            user_identity=Identity.from_event(event["userIdentity"]),
            s3=S3.from_event(event["s3"]),
        )


@dataclass
class S3Event:
    records: List[S3Record]

    @classmethod
    def from_event(cls, event: dict):
        return cls([S3Record.from_event(r) for r in event["Records"]])

    def get_bucket_and_key(self) -> Tuple[str, str]:
        """Get S3 bucket name and key.

        Returns:
            S3 bucket name and key
        """
        s3_record = self.records[0]
        return s3_record.s3.bucket.name, s3_record.s3.object.key
