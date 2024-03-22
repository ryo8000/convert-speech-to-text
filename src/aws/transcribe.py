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

"""Transcribe module."""

import os
import uuid
from datetime import (
    datetime,
)

import boto3


class TranscribeClient:
    DATETIME_FORMAT = "%Y%m%d%H%M%S"

    def __init__(self, client=None):
        """__init__ method.

        Args:
            client: transcribe client
        """
        self.client = client or boto3.client("transcribe")

    def start_transcription_job(
        self, current_datetime: datetime, src_object_url: str, language_code: str, dist_bucket: str, dist_key: str
    ) -> dict:
        """Start a transcription job.

        Args:
            current_datetime: current datetime
            src_object_url: S3 object url
            language_code: the language code that represents the language spoken in the input media file.
            dist_bucket: S3 bucket name of text data output destination
            dist_key: S3 key name of text data output destination

        Returns:
            data about the job
        """
        file_name = os.path.basename(src_object_url)
        ext = os.path.splitext(file_name)[1]
        transcription_file_name = f"{current_datetime.strftime(self.DATETIME_FORMAT)}_{uuid.uuid4()}_{file_name}"

        return self.client.start_transcription_job(
            TranscriptionJobName=transcription_file_name,
            LanguageCode=language_code,
            MediaFormat=ext[1:],
            Media={
                "MediaFileUri": src_object_url,
            },
            OutputBucketName=dist_bucket,
            OutputKey=f"{dist_key}/{transcription_file_name}.json",
        )
