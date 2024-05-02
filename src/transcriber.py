"""Transcriber module."""

import json
from datetime import datetime
from logging import getLogger

from aws.model import SqsEvent
from aws.transcribe import TranscribeClient
from config import Config

logger = getLogger(__name__)


def lambda_handler(event: dict, context) -> None:
    logger.debug(json.dumps(event))

    config = Config()
    current_datetime = datetime.now()
    transcribe_client = TranscribeClient()

    main(event, config, current_datetime, transcribe_client)


def main(event: dict, config: Config, current_datetime: datetime, transcribe_client: TranscribeClient):
    # process each message received by the SQS.
    sqs_event = SqsEvent.from_event(event)
    for s3_event in sqs_event.extract_s3_events():

        # create s3 object URL
        s3_object_url = s3_event.get_object_url()

        # start transcription job
        bucket = s3_event.get_bucket_and_key()[0]
        transcribe_client.start_transcription_job(
            current_datetime, s3_object_url, config.language_code, bucket, config.transcription_dist_key
        )
