import json
import os

from aws import s3, transcribe


def lambda_handler(event: dict, context) -> dict:
    print(json.dumps(event, ensure_ascii=False))

    bucket = os.environ["AWS_S3_BUCKET"]
    bucket_region = os.environ["AWS_S3_REGION"]
    src_dir = os.environ["AWS_S3_SRC_DIR"]
    body = event["body"]
    if body is None:
        return {
            'statusCode': 400,
            'body': json.dumps('error!', ensure_ascii=False)
        }
    uploaded_file = body.split("file=")[1]
    dist_dir = os.environ["AWS_S3_DIST_DIR"]

    # s3
    s3_object_url = s3.get_object_url(
        bucket, f"{src_dir}/{uploaded_file}", bucket_region)

    # transcribe
    language_code = "ja-JP"
    try:
        transcribe.start_transcription_job(
            s3_object_url, language_code, bucket, f"{dist_dir}/{uploaded_file}")
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('error!', ensure_ascii=False)
        }

    return {
        'statusCode': 200,
        'body': json.dumps('success!', ensure_ascii=False)
    }
