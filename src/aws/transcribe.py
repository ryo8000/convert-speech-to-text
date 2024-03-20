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

    def __init__(self, current_datetime: datetime, client=None):
        """__init__ method.

        Args:
            current_datetime: current datetime
            client: transcribe client
        """
        self.current_datetime = current_datetime
        self.client = client or boto3.client("transcribe")

    def start_transcription_job(self, src_object_url: str, language_code: str, dist_bucket: str, dist_key: str) -> dict:
        """Starts a transcription job.

        Args:
            src_object_url: S3 object url
            language_code: the language code that represents the language spoken in the input media file.
            dist_bucket: S3 bucket name of text data output destination
            dist_key: S3 key name of text data output destination

        Returns:
            data about the job
        """
        file_name = os.path.basename(src_object_url)
        file_name_without_ext, ext = os.path.splitext(file_name)
        file_name_prefix = f"{self.current_datetime.strftime(self.DATETIME_FORMAT)}_{uuid.uuid4()}_"

        response = self.client.start_transcription_job(
            TranscriptionJobName=f"{file_name_prefix}{file_name}",
            LanguageCode=language_code,
            MediaFormat=ext[1:],
            Media={
                "MediaFileUri": src_object_url,
            },
            OutputBucketName=dist_bucket,
            OutputKey=f"{dist_key}/{file_name_prefix}{file_name_without_ext}.json",
        )
        return response

    def create_uuid():
        return uuid.uuid4()
