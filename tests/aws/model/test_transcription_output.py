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

import json
import os
import unittest

from src.aws.model import Alternative, Item, Results, TranscribeOutput, Transcript


class TestTranscribeOutput(unittest.TestCase):

    def test_from_contents(self):
        contents = {}
        file_path = os.path.join(os.path.dirname(__file__), "..", "..", "events", "transcribe-output.json")
        with open(file_path) as file:
            contents = json.load(file)

        transcribe_output = TranscribeOutput.from_contents(contents)
        self.assertEqual(transcribe_output, TranscribeOutputFactory.create_transcribe_output())


class TranscribeOutputFactory:

    @staticmethod
    def create_transcribe_output() -> TranscribeOutput:
        return TranscribeOutput(
            job_name="my-first-transcription-job",
            account_id="111122223333",
            results=Results(
                transcripts=[Transcript(transcript="Welcome to Amazon Transcribe.")],
                items=[
                    Item(
                        start_time="0.64",
                        end_time="1.09",
                        alternatives=[Alternative(confidence="1.0", content="Welcome")],
                        type="pronunciation",
                    ),
                    Item(
                        start_time="1.09",
                        end_time="1.21",
                        alternatives=[Alternative(confidence="1.0", content="to")],
                        type="pronunciation",
                    ),
                    Item(
                        start_time="1.21",
                        end_time="1.74",
                        alternatives=[Alternative(confidence="1.0", content="Amazon")],
                        type="pronunciation",
                    ),
                    Item(
                        start_time="1.74",
                        end_time="2.56",
                        alternatives=[Alternative(confidence="1.0", content="Transcribe")],
                        type="pronunciation",
                    ),
                    Item(
                        start_time="",
                        end_time="",
                        alternatives=[Alternative(confidence="0.0", content=".")],
                        type="punctuation",
                    ),
                ],
            ),
            status="COMPLETED",
        )
