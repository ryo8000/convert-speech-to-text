"""AWS models package."""

from .s3_event import S3, Bucket, Identity, S3Event, S3Object, S3Record  # noqa
from .sqs_event import SqsEvent, SqsRecord  # noqa
from .transcribe_output import (  # noqa
    Alternative,
    Item,
    Results,
    TranscribeOutput,
    Transcript,
)
