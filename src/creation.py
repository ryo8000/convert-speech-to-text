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

"""Creation module."""

import json
import os
from logging import (
    INFO,
    getLogger,
)

from aws import (
    lambda_event,
    s3,
)
from aws.transcribe import (
    TranscribeClient,
)
from config import (
    Config,
)

logger = getLogger(__name__)
logger.setLevel(INFO)


def lambda_handler(event: dict, context) -> None:
    logger.info(json.dumps(event))
    config = Config()

    sqs_event = lambda_event.convert_dict_to_sqs_event(event)
    for sqs_record in sqs_event.records:
        s3_event = sqs_record.body
        if not s3_event:
            continue

        # retrieve the json file content output by the transcription job
        s3_record = s3_event.records[0]
        bucket = s3_record.s3.bucket.name
        key = s3_record.s3.object.key
        s3_client = s3.S3Client()
        json_contents = s3_client.get_json_contents(bucket, key)
        logger.info(json.dumps(json_contents))

        # txt
        transcript = json_contents["results"]["transcripts"][0]["transcript"]
        logger.info(transcript)

        file_name_without_ext = os.path.splitext(os.path.basename(key))[0]
        dist = f"{config.creation_dist_key}/{file_name_without_ext}.txt"
        s3_client.put_file(bucket, dist, transcript)

        # csv
        rows = ["start_time, end_time, content"]
        for item in json_contents["results"]["items"]:
            start_time = item.get("start_time", "")
            end_time = item.get("end_time", "")
            content = item["alternatives"][0]["content"]
            rows.append(f"{start_time}, {end_time}, {content}")

        dist = f"{config.creation_dist_key}/{file_name_without_ext}.csv"
        s3_client.put_file(bucket, dist, "\n".join(rows))

        # delete transcription job
        TranscribeClient().delete_transcription_job(file_name_without_ext)
