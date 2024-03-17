import json

from aws import (
    s3,
    sqs,
)
from aws.transcribe import (
    TranscribeClient,
)


def lambda_handler(event: dict, context) -> None:
    print(json.dumps(event))
    # bucket, key = s3.get_bucket_path(event)
    # print(bucket + '/' + key)

    # sqs
    body = sqs.get_message_info_list(event)[0]
    print(json.dumps(body))
    bucket, key = s3.get_bucket_path(body)

    # s3
    bucket_region = "ap-northeast-1"
    s3_object_url = s3.get_object_url(bucket, key, bucket_region)
    print(s3_object_url)

    # transcribe
    language_code = "ja-JP"
    dist_key = "t-output"
    try:
        result = TranscribeClient().start_transcription_job(
            s3_object_url, language_code, bucket, dist_key)
    except Exception as e:
        print(e)

    print(result)
