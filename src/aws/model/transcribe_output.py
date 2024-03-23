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

"""Transcribe output module."""

from dataclasses import dataclass
from typing import List


@dataclass
class Alternative:
    confidence: str
    content: str

    @classmethod
    def from_contents(cls, event: dict):
        return cls(confidence=event["confidence"], content=event["content"])


@dataclass
class Item:
    start_time: str
    end_time: str
    alternatives: List[Alternative]
    type: str

    @classmethod
    def from_contents(cls, event: dict):
        return cls(
            start_time=event.get("start_time", ""),
            end_time=event.get("end_time", ""),
            alternatives=[Alternative.from_contents(a) for a in event["alternatives"]],
            type=event["type"],
        )


@dataclass
class Transcript:
    transcript: str

    @classmethod
    def from_contents(cls, event: dict):
        return cls(transcript=event["transcript"])


@dataclass
class Results:
    transcripts: List[Transcript]
    items: List[Item]

    @classmethod
    def from_contents(cls, event: dict):
        return cls(
            transcripts=[Transcript.from_contents(t) for t in event["transcripts"]],
            items=[Item.from_contents(i) for i in event["items"]],
        )


@dataclass
class TranscribeOutput:
    job_name: str
    account_id: str
    results: Results
    status: str

    @classmethod
    def from_contents(cls, event: dict):
        return cls(
            job_name=event["jobName"],
            account_id=event["accountId"],
            results=Results.from_contents(event["results"]),
            status=event["status"],
        )

    def get_entire_transcript(self) -> str:
        """Get entire transcript

        Returns:
            entire transcript
        """
        return self.results.transcripts[0].transcript
