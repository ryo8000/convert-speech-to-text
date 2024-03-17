import json

import boto3

sqs_client = boto3.client("sqs")


def get_message_info_list(sqs_event: dict) -> list:
    que_info_list = []
    for record in sqs_event["Records"]:
        src_event = json.loads(record["body"])
        que_info_list.append(src_event)
    return que_info_list
