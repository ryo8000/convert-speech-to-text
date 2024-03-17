import json

from .model import (
    SqsEvent,
)


def convert_sqs_event(data: dict) -> SqsEvent:
    return SqsEvent(**data)


def get_message_info_list(sqs_event: dict) -> list:
    que_info_list = []
    for record in sqs_event["Records"]:
        src_event = json.loads(record["body"])
        que_info_list.append(src_event)
    return que_info_list
