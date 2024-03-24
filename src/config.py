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

"""Config module."""

import os


class Config:
    """Config class."""

    def __init__(self):
        """__init__ method."""
        self.transcription_dist_key = os.environ["AWS_S3_TRANSCRIPTION_DIST_KEY"]
        self.creation_dist_key = os.environ["AWS_S3_CREATION_DIST_KEY"]
        self.language_code = os.environ["AWS_TRANSCRIBE_LANGUAGE_CODE"]
