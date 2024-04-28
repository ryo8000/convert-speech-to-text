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

"""File creator module."""

import json
import os
import sys

from loguru import logger

from aws.model import SqsEvent, TranscribeOutput
from aws.s3 import S3Client
from aws.transcribe import TranscribeClient
from config import Config

config = Config()
logger.remove(0)
logger.add(sys.stderr, level=config.lambda_log_level)


def lambda_handler(event: dict, context) -> None:
    logger.info(json.dumps(event))

    s3_client = S3Client()
    transcribe_client = TranscribeClient()

    main(event, config, s3_client, transcribe_client)


def main(event: dict, config: Config, s3_client: S3Client, transcribe_client: TranscribeClient):
    # process each message received by the SQS.
    sqs_event = SqsEvent.from_event(event)
    for s3_event in sqs_event.extract_s3_events():

        # retrieve the json file content output by the transcription job
        bucket, key = s3_event.get_bucket_and_key()
        json_contents = s3_client.get_json_contents(bucket, key)
        logger.debug(json.dumps(json_contents))
        transcribe_output = TranscribeOutput.from_contents(json_contents)

        # create csv contents
        rows = ["start_time, end_time, content", f", , {transcribe_output.get_entire_transcript()}"]
        for item in transcribe_output.results.items:
            rows.append(f"{item.start_time}, {item.end_time}, {item.alternatives[0].content}")

        # create csv file
        file_name_without_ext = os.path.splitext(os.path.basename(key))[0]
        dist = f"{config.creation_dist_key}/{file_name_without_ext}.csv"
        s3_client.put_file(bucket, dist, "\n".join(rows))
        logger.info(dist)

        # delete transcription job
        transcribe_client.delete_transcription_job(file_name_without_ext)
