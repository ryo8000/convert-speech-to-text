"""SQS event module."""

import json
from dataclasses import dataclass
from typing import Generator, List, Optional

from .s3_event import S3Event


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

    def extract_s3_events(self) -> Generator[S3Event, None, None]:
        """Extract normal s3 events

        Returns:
            Extracted s3 events
        """
        for record in self.records:
            if record.body is None:
                continue
            yield record.body
