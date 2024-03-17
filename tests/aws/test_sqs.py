# Copyright 2024 Ryo H
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from src.aws import (
    sqs,
)


class TestSqs(unittest.TestCase):
    def setUp(self):
        self.event = {
            "Records": [
                {
                    "messageId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                    "receiptHandle": "abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890ab",
                    "body": '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"ap-northeast-1","eventTime":"2024-03-17T02:13:16.960Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:ABCDE67890ABCDE67890A"},"requestParameters":{"sourceIPAddress":"xxx.xxx.xxx.xxx"},"responseElements":{"x-amz-request-id":"ABCDE67890ABCDE6","x-amz-id-2":"abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde678"},"s3":{"s3SchemaVersion":"1.0","configurationId":"MyEvent","bucket":{"name":"my-bucket","ownerIdentity":{"principalId":"ABCDE67890ABCD"},"arn":"arn:aws:s3:::my-bucket"},"object":{"key":"input/audiofile.mp3","size":668536,"eTag":"abcde67890abcde67890abcde67890ab","sequencer":"ABCDE67890ABCDE678"}}}]}',
                    "attributes": {
                        "ApproximateReceiveCount": "1",
                        "SentTimestamp": "1710641597828",
                        "SenderId": "ABCDE67890ABCDE67890A:S3-PROD-END",
                        "ApproximateFirstReceiveTimestamp": "1710641597831",
                    },
                    "messageAttributes": {},
                    "md5OfBody": "abcde67890abcde67890abcde67890ab",
                    "eventSource": "aws:sqs",
                    "eventSourceARN": "arn:aws:sqs:ap-northeast-1:xxxxxxxxxxxx:MyQueue",
                    "awsRegion": "ap-northeast-1",
                }
            ]
        }

    def test_convert_sqs_event(self):
        sqs_event = sqs.convert_sqs_event(self.event)

        self.assertEqual(sqs_event.Records[0].messageId, "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        self.assertEqual(
            sqs_event.Records[0].receiptHandle,
            "abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890ab",
        )
        self.assertEqual(
            sqs_event.Records[0].body,
            "{\"Records\":[{\"eventVersion\":\"2.1\",\"eventSource\":\"aws:s3\",\"awsRegion\":\"ap-northeast-1\",\"eventTime\":\"2024-03-17T02:13:16.960Z\",\"eventName\":\"ObjectCreated:Put\",\"userIdentity\":{\"principalId\":\"AWS:ABCDE67890ABCDE67890A\"},\"requestParameters\":{\"sourceIPAddress\":\"xxx.xxx.xxx.xxx\"},\"responseElements\":{\"x-amz-request-id\":\"ABCDE67890ABCDE6\",\"x-amz-id-2\":\"abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde67890abcde678\"},\"s3\":{\"s3SchemaVersion\":\"1.0\",\"configurationId\":\"MyEvent\",\"bucket\":{\"name\":\"my-bucket\",\"ownerIdentity\":{\"principalId\":\"ABCDE67890ABCD\"},\"arn\":\"arn:aws:s3:::my-bucket\"},\"object\":{\"key\":\"input/audiofile.mp3\",\"size\":668536,\"eTag\":\"abcde67890abcde67890abcde67890ab\",\"sequencer\":\"ABCDE67890ABCDE678\"}}}]}"
        )
        self.assertEqual(sqs_event.Records[0].attributes.ApproximateReceiveCount, "1")
        self.assertEqual(sqs_event.Records[0].attributes.SentTimestamp, "1710641597828")
        self.assertEqual(sqs_event.Records[0].attributes.SenderId, "ABCDE67890ABCDE67890A:S3-PROD-END")
        self.assertEqual(sqs_event.Records[0].attributes.ApproximateFirstReceiveTimestamp, "1710641597831")
        self.assertEqual(sqs_event.Records[0].md5OfBody, "abcde67890abcde67890abcde67890ab")
        self.assertEqual(sqs_event.Records[0].eventSource, "aws:sqs")
        self.assertEqual(sqs_event.Records[0].eventSourceARN, "arn:aws:sqs:ap-northeast-1:xxxxxxxxxxxx:MyQueue")
        self.assertEqual(sqs_event.Records[0].awsRegion, "ap-northeast-1")
