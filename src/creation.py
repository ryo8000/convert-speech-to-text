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

from aws import (
    s3,
    sqs,
)


def lambda_handler(event: dict, context) -> None:
    print(json.dumps(event))

    # sqs
    body = sqs.get_message_info_list(event)[0]
    print(json.dumps(body))
    bucket, key = s3.get_bucket_path(body)

    # s3
    s3_client = s3.S3Client()
    json_contents = s3_client.get_json_contents(bucket, key)
    print(json.dumps(json_contents))

    transcript = json_contents["results"]["transcripts"][0]["transcript"]
    print(transcript)

    file_name_without_ext = os.path.splitext(os.path.basename(key))[0]
    dist = f"t-output/{file_name_without_ext}.txt"
    s3_client.put_file(bucket, dist, transcript)
