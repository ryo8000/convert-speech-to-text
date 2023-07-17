import os

import boto3

client = boto3.client("transcribe")


def start_transcription_job(src_bucket: str, src_key: str, src_bucket_region: str, language_code: str, dist_bucket: str, dist_key: str) -> dict:
    """Starts a transcription job.

    Args:
        src_bucket: S3 bucket name of the audio file
        src_key: S3 key name of the audio file
        src_bucket_region: S3 bucket region
        language_code: the language code that represents the language spoken in the input media file.
        dist_bucket: S3 bucket name of text data output destination
        dist_key: S3 key name of text data output destination

    Returns:
        data about the job
    """
    region = f"{src_bucket_region}." if src_bucket_region != "us-east-1" else ""
    file_uri = f"https://{src_bucket}.s3.{region}amazonaws.com/{src_key}"

    file_name = os.path.basename(src_key)
    file_name_without_ext, ext = os.path.splitext(file_name)

    response = client.start_transcription_job(
        TranscriptionJobName=f"{src_bucket}-{file_name}",
        LanguageCode=language_code,
        MediaFormat=ext[1:],
        Media={
            "MediaFileUri": file_uri,
        },
        OutputBucketName=dist_bucket,
        OutputKey=f"{dist_key}/{file_name_without_ext}.json",
    )
    return response
