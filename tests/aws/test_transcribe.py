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
        self.target = TranscribeClient(client=boto3.client("transcribe", region_name="us-west-1"))

    @mock_aws
    def test_start_transcription_job(self):
        ext = "mp3"
        filename = f"audiofile.{ext}"
        src_object_url = f"https://src-bucket.s3.us-west-1.amazonaws.com/input/{filename}"
        language_code = "en-US"

        response = self.target.start_transcription_job(
            src_object_url=src_object_url,
            language_code=language_code,
            dist_bucket="dist-bucket",
            dist_key="output"
        )
        self.assertIn("TranscriptionJob", response)
        self.assertEqual(response["TranscriptionJob"]["TranscriptionJobName"], filename)
        self.assertEqual(response["TranscriptionJob"]["LanguageCode"], language_code)
        self.assertEqual(response["TranscriptionJob"]["MediaFormat"], ext)
        self.assertEqual(response["TranscriptionJob"]["Media"]["MediaFileUri"], src_object_url)
