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

"""Common utilities used by the MCP server."""

from typing import Any, Dict, Mapping, Union

from google.analytics import admin_v1beta, data_v1beta, admin_v1alpha
from google.api_core.gapic_v1.client_info import ClientInfo
from google.auth import credentials as auth_credentials
from google.auth.credentials import with_scopes_if_required
from importlib import metadata
from pathlib import Path
import google.auth
import json
import os
import proto
from google.oauth2 import service_account


def _get_package_version_with_fallback():
    """Returns the version of the package.

    Falls back to 'unknown' if the version can't be resolved.
    """
    try:
        return metadata.version("analytics-mcp")
    except:
        return "unknown"


# Client information that adds a custom user agent to all API requests.
_CLIENT_INFO = ClientInfo(
    user_agent=f"analytics-mcp/{_get_package_version_with_fallback()}"
)

# Read-only scope for Analytics Admin API and Analytics Data API.
_READ_ONLY_ANALYTICS_SCOPE = (
    "https://www.googleapis.com/auth/analytics.readonly"
)


CredentialsLike = Union[
    auth_credentials.Credentials, Mapping[str, Any], str, None
]


def _create_credentials() -> auth_credentials.Credentials:
    """Returns Application Default Credentials with read-only scope."""
    (credentials, _) = google.auth.default(scopes=[_READ_ONLY_ANALYTICS_SCOPE])
    return credentials


def _load_service_account_info(
    credentials_source: Union[Mapping[str, Any], str]
) -> Dict[str, Any]:
    """Loads service account information from a mapping, JSON string, or file path."""
    if isinstance(credentials_source, Mapping):
        return dict(credentials_source)

    if isinstance(credentials_source, str):
        candidate = credentials_source.strip()
        # First, try to interpret the string as JSON.
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            path = Path(candidate).expanduser()
            if not path.is_file():
                raise ValueError(
                    "Unable to parse provided credentials. "
                    "Expected a JSON object/string or a path to a service account JSON file."
                )
            try:
                return json.loads(path.read_text())
            except json.JSONDecodeError as err:
                raise ValueError(
                    f"Credentials file at '{path}' does not contain valid JSON."
                ) from err

    raise TypeError(
        "Unsupported credential override type. "
        "Provide a google.auth.credentials.Credentials instance, "
        "a mapping, a JSON string, or a path to a JSON key file."
    )


def _resolve_credentials(
    credentials_override: CredentialsLike = None,
) -> auth_credentials.Credentials:
    """Returns credentials computed from the override or raises if none provided."""
    if credentials_override is None:
        if os.getenv("ANALYTICS_MCP_ALLOW_ADC", "").lower() in (
            "1",
            "true",
            "yes",
            "on",
        ):
            return _create_credentials()
        raise RuntimeError(
            "No credentials supplied. Pass the 'credentials' argument or set "
            "ANALYTICS_MCP_ALLOW_ADC=true to permit Application Default Credentials."
        )

    if isinstance(credentials_override, auth_credentials.Credentials):
        return with_scopes_if_required(
            credentials_override, [_READ_ONLY_ANALYTICS_SCOPE]
        )

    service_account_info = _load_service_account_info(credentials_override)
    return service_account.Credentials.from_service_account_info(
        service_account_info, scopes=[_READ_ONLY_ANALYTICS_SCOPE]
    )


def create_admin_api_client(
    credentials_override: CredentialsLike = None,
) -> admin_v1beta.AnalyticsAdminServiceAsyncClient:
    """Returns a properly configured Google Analytics Admin API async client.

    Uses Application Default Credentials with read-only scope unless a specific
    credential override is supplied.
    """
    return admin_v1beta.AnalyticsAdminServiceAsyncClient(
        client_info=_CLIENT_INFO,
        credentials=_resolve_credentials(credentials_override),
    )


def create_data_api_client(
    credentials_override: CredentialsLike = None,
) -> data_v1beta.BetaAnalyticsDataAsyncClient:
    """Returns a properly configured Google Analytics Data API async client.

    Uses Application Default Credentials with read-only scope unless a specific
    credential override is supplied.
    """
    return data_v1beta.BetaAnalyticsDataAsyncClient(
        client_info=_CLIENT_INFO,
        credentials=_resolve_credentials(credentials_override),
    )


def create_admin_alpha_api_client(
    credentials_override: CredentialsLike = None,
) -> (
    admin_v1alpha.AnalyticsAdminServiceAsyncClient
):
    """Returns a properly configured Google Analytics Admin API (alpha) async client.
    Uses Application Default Credentials with read-only scope unless a specific
    credential override is supplied.
    """
    return admin_v1alpha.AnalyticsAdminServiceAsyncClient(
        client_info=_CLIENT_INFO,
        credentials=_resolve_credentials(credentials_override),
    )


def construct_property_rn(property_value: int | str) -> str:
    """Returns a property resource name in the format required by APIs."""
    property_num = None
    if isinstance(property_value, int):
        property_num = property_value
    elif isinstance(property_value, str):
        property_value = property_value.strip()
        if property_value.isdigit():
            property_num = int(property_value)
        elif property_value.startswith("properties/"):
            numeric_part = property_value.split("/")[-1]
            if numeric_part.isdigit():
                property_num = int(numeric_part)
    if property_num is None:
        raise ValueError(
            (
                f"Invalid property ID: {property_value}. "
                "A valid property value is either a number or a string starting "
                "with 'properties/' and followed by a number."
            )
        )

    return f"properties/{property_num}"


def proto_to_dict(obj: proto.Message) -> Dict[str, Any]:
    """Converts a proto message to a dictionary."""
    return type(obj).to_dict(
        obj, use_integers_for_enums=False, preserving_proto_field_name=True
    )


def proto_to_json(obj: proto.Message) -> str:
    """Converts a proto message to a JSON string."""
    return type(obj).to_json(obj, indent=None, preserving_proto_field_name=True)
