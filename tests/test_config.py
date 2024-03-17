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

import os
import unittest
from unittest.mock import (
    patch,
)

from src.config import (
    Config,
)


class TestConfig(unittest.TestCase):
    @patch.dict(
        os.environ,
        {
            "AWS_S3_BUCKET": "test-bucket",
            "AWS_S3_BUCKET_REGION": "us-east-1",
            "AWS_S3_TRANSCRIPTION_DIST_KEY": "transcription-dist-key",
            "AWS_S3_CREATION_DIST_KEY": "creation-dist-key",
            "AWS_TRANSCRIBE_LANGUAGE_CODE": "en-US",
        },
    )
    def test_config_creation_with_valid_env_variables(self):
        config = Config()
        self.assertEqual(config.bucket, "test-bucket")
        self.assertEqual(config.bucket_region, "us-east-1")
        self.assertEqual(config.transcription_dist_key, "transcription-dist-key")
        self.assertEqual(config.creation_dist_key, "creation-dist-key")
        self.assertEqual(config.language_code, "en-US")

    @patch.dict(os.environ, {}, clear=True)
    def test_config_creation_without_env_variables(self):
        with self.assertRaises(KeyError):
            Config()
