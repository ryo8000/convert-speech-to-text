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

import unittest
import uuid
from datetime import (
    datetime,
)
from unittest.mock import (
    patch,
)

import boto3
from moto import (
    mock_aws,
)

from src.aws.transcribe import (
    TranscribeClient,
)


class TestTranscribeClient(unittest.TestCase):
    @mock_aws
    def setUp(self):
        date_time = datetime.strptime("2024-02-29 23:59:59.999999", "%Y-%m-%d %H:%M:%S.%f")
        self.target = TranscribeClient(
            current_datetime=date_time, client=boto3.client("transcribe", region_name="us-west-1")
        )

    @mock_aws
    @patch("uuid.uuid4")
    def test_start_transcription_job(self, mock_uuid4):
        expected_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        mock_uuid4.return_value = expected_uuid

        src_object_url = "https://src-bucket.s3.us-west-1.amazonaws.com/input/audiofile.mp3"

        response = self.target.start_transcription_job(
            src_object_url=src_object_url,
            language_code="en-US",
            dist_bucket="dist-bucket",
            dist_key="output",
        )
        self.assertIn("TranscriptionJob", response)
        self.assertEqual(
            response["TranscriptionJob"]["TranscriptionJobName"], f"20240229235959_{expected_uuid}_audiofile.mp3"
        )
        self.assertEqual(response["TranscriptionJob"]["LanguageCode"], "en-US")
        self.assertEqual(response["TranscriptionJob"]["MediaFormat"], "mp3")
        self.assertEqual(response["TranscriptionJob"]["Media"]["MediaFileUri"], src_object_url)
