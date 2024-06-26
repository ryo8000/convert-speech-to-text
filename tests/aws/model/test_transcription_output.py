import json
import os
import unittest

from src.aws.model import Alternative, Item, Results, TranscribeOutput, Transcript


class TestTranscribeOutput(unittest.TestCase):

    def setUp(self):
        self.transcribe_output = TranscribeOutputFactory.create_transcribe_output()

    def test_from_contents(self):
        contents = {}
        file_path = os.path.join(os.path.dirname(__file__), "..", "..", "events", "transcribe-output.json")
        with open(file_path) as file:
            contents = json.load(file)

        transcribe_output = TranscribeOutput.from_contents(contents)
        self.assertEqual(transcribe_output, self.transcribe_output)

    def test_get_entire_transcript(self):
        self.assertEqual(self.transcribe_output.get_entire_transcript(), "Welcome to Amazon Transcribe.")


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
