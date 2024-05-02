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
        """Get bucket name and key.

        Returns:
            bucket name and key
        """
        record = self.records[0]
        return record.s3.bucket.name, record.s3.object.key

    def get_object_url(self) -> str:
        """Get the object url.

        Returns:
           the object url
        """
        record = self.records[0]
        bucket_region = f"{record.aws_region}." if record.aws_region != "us-east-1" else ""
        return f"https://{record.s3.bucket.name}.s3.{bucket_region}amazonaws.com/{record.s3.object.key}"
