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
