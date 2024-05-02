import unittest
import uuid
from datetime import datetime
from unittest.mock import patch

import boto3
from moto import mock_aws

from src.aws.transcribe import TranscribeClient


class TestTranscribeClient(unittest.TestCase):
    @mock_aws
    def setUp(self):
        self.client = TranscribeClient(client=boto3.client("transcribe", region_name="us-west-1"))

    @mock_aws
    @patch("uuid.uuid4")
    def test_start_transcription_job(self, mock_uuid4):
        expected_uuid = uuid.UUID("12345678-1234-5678-1234-567812345678")
        mock_uuid4.return_value = expected_uuid

        src_object_url = "https://src-bucket.s3.us-west-1.amazonaws.com/input/audiofile.mp3"

        response = self.client.start_transcription_job(
            datetime.strptime("2024-02-29 23:59:59.999999", "%Y-%m-%d %H:%M:%S.%f"),
            src_object_url,
            "en-US",
            "dist-bucket",
            "output",
        )
        self.assertIn("TranscriptionJob", response)
        self.assertEqual(
            response["TranscriptionJob"]["TranscriptionJobName"], f"20240229235959_{expected_uuid}_audiofile.mp3"
        )
        self.assertEqual(response["TranscriptionJob"]["LanguageCode"], "en-US")
        self.assertEqual(response["TranscriptionJob"]["MediaFormat"], "mp3")
        self.assertEqual(response["TranscriptionJob"]["Media"]["MediaFileUri"], src_object_url)
