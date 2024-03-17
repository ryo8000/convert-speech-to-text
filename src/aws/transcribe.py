import os

import boto3


class TranscribeClient:
    def __init__(self, client=None):
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

        response = self.client.start_transcription_job(
            TranscriptionJobName=file_name,
            LanguageCode=language_code,
            MediaFormat=ext[1:],
            Media={
                "MediaFileUri": src_object_url,
            },
            OutputBucketName=dist_bucket,
            OutputKey=f"{dist_key}/{file_name_without_ext}.json",
        )
        return response
