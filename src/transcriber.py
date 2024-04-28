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

"""Transcriber module."""

import json
import sys
from datetime import datetime

from loguru import logger

from aws.model import SqsEvent
from aws.transcribe import TranscribeClient
from config import Config

config = Config()
logger.remove(0)
logger.add(sys.stderr, level=config.lambda_log_level)


def lambda_handler(event: dict, context) -> None:
    logger.info(json.dumps(event))

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
