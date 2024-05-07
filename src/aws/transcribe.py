"""Transcribe module."""

import os
import uuid
from datetime import datetime

import boto3


class TranscribeClient:
    DATETIME_FORMAT = "%Y%m%d%H%M%S"

    def __init__(self, client=None):
        """__init__ method.

        Args:
            client (optional): transcribe client
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
            result of starting a transcription job
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

    def delete_transcription_job(self, job_name: str) -> dict:
        """Delete a transcription job.

        Args:
            job_name: job to be deleted

        Returns:
            result of deletion a transcription job
        """
        return self.client.delete_transcription_job(TranscriptionJobName=job_name)
