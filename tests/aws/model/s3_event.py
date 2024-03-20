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

from src.aws.model import (
    S3,
    Bucket,
    Identity,
    S3Event,
    S3Object,
    S3Record,
)


class S3EventFactory:

    @staticmethod
    def create_s3_event() -> S3Event:
        return S3Event(
            records=[
                S3Record(
                    event_version="2.1",
                    event_source="aws:s3",
                    aws_region="ap-northeast-1",
                    event_time="2024-03-17T02:13:16.960Z",
                    event_name="ObjectCreated:Put",
                    user_identity=Identity(principal_id="AWS:ABCDE67890ABCDE67890A"),
                    s3=S3(
                        s3_schema_version="1.0",
                        configuration_id="MyEvent",
                        bucket=Bucket(
                            name="my-bucket",
                            owner_identity=Identity(principal_id="ABCDE67890ABCD"),
                            arn="arn:aws:s3:::my-bucket",
                        ),
                        object=S3Object(
                            key="input/audiofile.mp3",
                            size=668536,
                            e_tag="abcde67890abcde67890abcde67890ab",
                            sequencer="ABCDE67890ABCDE678",
                        ),
                    ),
                )
            ]
        )
