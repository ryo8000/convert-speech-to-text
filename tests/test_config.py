import os
import unittest
from unittest.mock import patch

from src.config import Config


class TestConfig(unittest.TestCase):

    @patch.dict(
        os.environ,
        {
            "AWS_S3_TRANSCRIPTION_DIST_KEY": "transcription-dist-key",
            "AWS_S3_CREATION_DIST_KEY": "creation-dist-key",
            "AWS_TRANSCRIBE_LANGUAGE_CODE": "en-US",
        },
    )
    def test_config_creation_with_valid_env_variables(self):
        config = Config()
        self.assertEqual(config.transcription_dist_key, "transcription-dist-key")
        self.assertEqual(config.creation_dist_key, "creation-dist-key")
        self.assertEqual(config.language_code, "en-US")

    @patch.dict(os.environ, {}, clear=True)
    def test_config_creation_without_env_variables(self):
        with self.assertRaises(KeyError):
            Config()
