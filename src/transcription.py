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

"""Transcription module."""

import json
from datetime import datetime
from logging import INFO, getLogger

from aws import lambda_event, s3
from aws.transcribe import TranscribeClient
from config import Config

logger = getLogger(__name__)
logger.setLevel(INFO)


def lambda_handler(event: dict, context) -> None:
    logger.info(json.dumps(event))

    config = Config()
    current_datetime = datetime.now()
    transcribe_client = TranscribeClient()

    main(event, config, current_datetime, transcribe_client)


def main(event: dict, config: Config, current_datetime: datetime, transcribe_client: TranscribeClient):
    # Process each message received by the SQS.
    sqs_event = lambda_event.convert_dict_to_sqs_event(event)
    for sqs_record in sqs_event.records:
        s3_event = sqs_record.body
        if not s3_event:
            continue

        # create s3 object URL
        s3_record = s3_event.records[0]
        bucket = s3_record.s3.bucket.name
        key = s3_record.s3.object.key
        s3_object_url = s3.get_object_url(bucket, key, config.bucket_region)
        logger.info(s3_object_url)

        # start transcription job
        transcribe_client.start_transcription_job(
            current_datetime, s3_object_url, config.language_code, bucket, config.transcription_dist_key
        )
