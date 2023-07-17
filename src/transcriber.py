from aws import s3, transcribe


def lambda_handler(event: dict, context) -> None:
    bucket, key = s3.get_bucket_path(event)

    region = "ap-northeast-1"
    s3_object_url = s3.get_object_url(bucket, key, region)

    language_code = "ja-JP"
    dist_key = "foo"
    try:
        transcribe.start_transcription_job(s3_object_url, language_code, bucket, dist_key)
    except Exception as e:
        print(e)
