"""Config module."""

import os


class Config:
    """Config class."""

    def __init__(self):
        """__init__ method."""
        self.transcription_dist_key = os.environ["AWS_S3_TRANSCRIPTION_DIST_KEY"]
        self.creation_dist_key = os.environ["AWS_S3_CREATION_DIST_KEY"]
        self.language_code = os.environ["AWS_TRANSCRIBE_LANGUAGE_CODE"]
