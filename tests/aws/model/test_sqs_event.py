import json
import os
import unittest

from src.aws.model import SqsEvent, SqsRecord

from .test_s3_event import S3EventFactory


class TestSqsEvent(unittest.TestCase):

    def setUp(self):
        self.sqs_event = SqsEventFactory.create_sqs_event()

    def test_from_event(self):
        contents = {}
        file_path = os.path.join(os.path.dirname(__file__), "..", "..", "events", "sqs-event.json")
        with open(file_path) as file:
            contents = json.load(file)

        sqs_event = SqsEvent.from_event(contents)
        self.assertEqual(sqs_event, self.sqs_event)

    def test_extract_s3_events(self):
        s3_events = [s3_event for s3_event in self.sqs_event.extract_s3_events()]
        self.assertEqual(s3_events, [S3EventFactory.create_s3_event()])


class SqsEventFactory:

    @staticmethod
    def create_sqs_event() -> SqsEvent:
        return SqsEvent(
            records=[
                SqsRecord(
                    messageId="059f36b4-87a3-44ab-83d2-661975830a7d",
                    body=S3EventFactory.create_s3_event(),  # normal event
                ),
                SqsRecord(
                    messageId="2e1424d4-f796-459a-8184-9c92662be6da",
                    body=None,  # abnormal event
                ),
            ]
        )
