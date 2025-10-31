# Copyright 2025 Google LLC All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test cases for the utils module."""

import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from analytics_mcp.tools import utils
from google.auth import credentials as auth_credentials


class TestUtils(unittest.TestCase):
    """Test cases for the utils module."""

    def test_construct_property_rn(self):
        """Tests construct_property_rn using valid input."""
        self.assertEqual(
            utils.construct_property_rn(12345),
            "properties/12345",
            "Numeric property ID should b considered valid",
        )
        self.assertEqual(
            utils.construct_property_rn("12345"),
            "properties/12345",
            "Numeric property ID as string should be considered valid",
        )
        self.assertEqual(
            utils.construct_property_rn(" 12345  "),
            "properties/12345",
            "Whitespace around property ID should be considered valid",
        )
        self.assertEqual(
            utils.construct_property_rn("properties/12345"),
            "properties/12345",
            "Full resource name should be considered valid",
        )

    def test_construct_property_rn_invalid_input(self):
        """Tests that construct_property_rn raises a ValueError for invalid input."""
        with self.assertRaises(ValueError, msg="None should fail"):
            utils.construct_property_rn(None)
        with self.assertRaises(ValueError, msg="Empty string should fail"):
            utils.construct_property_rn("")
        with self.assertRaises(
            ValueError, msg="Non-numeric string should fail"
        ):
            utils.construct_property_rn("abc")
        with self.assertRaises(
            ValueError, msg="Resource name without ID should fail"
        ):
            utils.construct_property_rn("properties/")
        with self.assertRaises(
            ValueError, msg="Resource name with non-numeric ID should fail"
        ):
            utils.construct_property_rn("properties/abc")
        with self.assertRaises(
            ValueError,
            msg="Resource name with more than 2 components should fail",
        ):
            utils.construct_property_rn("properties/123/abc")

    def test_load_service_account_info_with_mapping(self):
        """Mapping input should be returned as a new dictionary."""
        mapping = {"type": "service_account", "project_id": "proj"}
        result = utils._load_service_account_info(mapping)
        self.assertEqual(result, mapping)
        self.assertIsNot(result, mapping, "Result should be a copy, not the original mapping")

    def test_load_service_account_info_with_json_string(self):
        """JSON string input should be parsed into a dictionary."""
        payload = {"type": "service_account", "project_id": "proj"}
        result = utils._load_service_account_info(json.dumps(payload))
        self.assertEqual(result, payload)

    def test_load_service_account_info_with_file_path(self):
        """File path input should load JSON content."""
        payload = {"type": "service_account", "project_id": "proj"}
        with tempfile.NamedTemporaryFile("w", delete=False) as tmp:
            json.dump(payload, tmp)
            tmp_path = tmp.name
        try:
            result = utils._load_service_account_info(tmp_path)
            self.assertEqual(result, payload)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

    def test_load_service_account_info_with_invalid_string(self):
        """Non-existent paths should raise a ValueError."""
        with self.assertRaises(ValueError):
            utils._load_service_account_info("nonexistent_credentials.json")

    def test_resolve_credentials_requires_override_by_default(self):
        """Without overrides or env flags, credentials must be supplied."""
        with self.assertRaises(RuntimeError):
            utils._resolve_credentials()

    @mock.patch("analytics_mcp.tools.utils.with_scopes_if_required")
    def test_resolve_credentials_with_credentials_instance(self, mock_with_scopes):
        """Credentials overrides should be scoped if required."""
        supplied_credentials = mock.create_autospec(auth_credentials.Credentials)
        scoped_credentials = mock.Mock()
        mock_with_scopes.return_value = scoped_credentials

        resolved = utils._resolve_credentials(supplied_credentials)

        mock_with_scopes.assert_called_once()
        self.assertIs(resolved, scoped_credentials)

    @mock.patch("analytics_mcp.tools.utils.service_account.Credentials.from_service_account_info")
    def test_resolve_credentials_with_mapping_override(self, mock_from_info):
        """Mappings should be converted into service account credentials."""
        mapping = {"type": "service_account", "project_id": "proj"}
        fake_credentials = mock.create_autospec(auth_credentials.Credentials)
        mock_from_info.return_value = fake_credentials

        resolved = utils._resolve_credentials(mapping)

        mock_from_info.assert_called_once()
        self.assertIs(resolved, fake_credentials)

    @mock.patch("analytics_mcp.tools.utils.google.auth.default")
    def test_resolve_credentials_env_flag_allows_adc(self, mock_default):
        """Setting ANALYTICS_MCP_ALLOW_ADC should fall back to ADC."""
        fake_credentials = mock.create_autospec(auth_credentials.Credentials)
        mock_default.return_value = (fake_credentials, None)

        with mock.patch.dict(
            "os.environ", {"ANALYTICS_MCP_ALLOW_ADC": "true"}, clear=False
        ):
            resolved = utils._resolve_credentials()

        self.assertIs(resolved, fake_credentials)
        mock_default.assert_called_once()
