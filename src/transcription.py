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

from aws import (
    s3,
    sqs,
)
from aws.transcribe import (
    TranscribeClient,
)
from config import (
    Config,
)


def lambda_handler(event: dict, context) -> None:
    print(json.dumps(event))
    config = Config()

    # sqs
    body = sqs.get_message_info_list(event)[0]
    print(json.dumps(body))
    if "s3:TestEvent" in body:
        return
    bucket, key = s3.get_bucket_path(body)

    # s3
    s3_object_url = s3.get_object_url(bucket, key, config.bucket_region)
    print(s3_object_url)

    # transcribe
    try:
        result = TranscribeClient().start_transcription_job(
            s3_object_url, config.language_code, bucket, config.transcription_dist_key
        )
    except Exception as e:
        print(e)

    print(result)
