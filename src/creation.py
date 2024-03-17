import json
import os

from aws import (
    s3,
    sqs,
)


def lambda_handler(event: dict, context) -> None:
    print(json.dumps(event))

    # sqs
    body = sqs.get_message_info_list(event)[0]
    print(json.dumps(body))
    bucket, key = s3.get_bucket_path(body)

    # s3
    s3_client = s3.S3Client()
    json_contents = s3_client.get_json_contents(bucket, key)
    print(json.dumps(json_contents))

    transcript = json_contents["results"]["transcripts"][0]["transcript"]
    print(transcript)

    file_name_without_ext = os.path.splitext(os.path.basename(key))[0]
    dist = f"t-output/{file_name_without_ext}.txt"
    s3_client.put_file(bucket, dist, transcript)
