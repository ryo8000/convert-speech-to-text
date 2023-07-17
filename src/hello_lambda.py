from aws import s3, transcribe


def lambda_handler(event: dict, context) -> None:

    bucket, key = s3.get_bucket_path(event)

    region = "ap-northeast-1"
    language_code = "ja-JP"
    dist_key = "foo"

    try:
        transcribe.start_transcription_job(bucket, key, region, language_code, bucket, dist_key)
    except Exception as e:
        print(e)
