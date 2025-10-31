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

"""Tools for gathering Google Analytics account and property information."""

from typing import Any, Dict, List

from analytics_mcp.coordinator import mcp
from analytics_mcp.tools.utils import (
    CredentialsLike,
    construct_property_rn,
    create_admin_api_client,
    create_admin_alpha_api_client,
    proto_to_dict,
)
from google.analytics import admin_v1beta, admin_v1alpha


@mcp.tool()
async def get_account_summaries(
    credentials: CredentialsLike = None,
) -> List[Dict[str, Any]]:
    """Retrieves information about the user's Google Analytics accounts and properties.

    Args:
        credentials: Optional override for the credentials used to call the
          Analytics Admin API. Provide a google.auth.credentials.Credentials
          instance, a mapping/dict with service account JSON, a JSON string, or
          a path to a service account key file.
    """

    # Uses an async list comprehension so the pager returned by
    # list_account_summaries retrieves all pages.
    summary_pager = await create_admin_api_client(
        credentials_override=credentials
    ).list_account_summaries()
    all_pages = [
        proto_to_dict(summary_page) async for summary_page in summary_pager
    ]
    return all_pages


@mcp.tool(title="List links to Google Ads accounts")
async def list_google_ads_links(
    property_id: int | str, credentials: CredentialsLike = None
) -> List[Dict[str, Any]]:
    """Returns a list of links to Google Ads accounts for a property.

    Args:
        property_id: The Google Analytics property ID. Accepted formats are:
          - A number
          - A string consisting of 'properties/' followed by a number
        credentials: Optional override for the credentials used to call the
          Analytics Admin API. Provide a google.auth.credentials.Credentials
          instance, a mapping/dict with service account JSON, a JSON string, or
          a path to a service account key file.
    """
    request = admin_v1beta.ListGoogleAdsLinksRequest(
        parent=construct_property_rn(property_id)
    )
    # Uses an async list comprehension so the pager returned by
    # list_google_ads_links retrieves all pages.
    links_pager = await create_admin_api_client(
        credentials_override=credentials
    ).list_google_ads_links(request=request)
    all_pages = [proto_to_dict(link_page) async for link_page in links_pager]
    return all_pages


@mcp.tool(title="Gets details about a property")
async def get_property_details(
    property_id: int | str, credentials: CredentialsLike = None
) -> Dict[str, Any]:
    """Returns details about a property.
    Args:
        property_id: The Google Analytics property ID. Accepted formats are:
          - A number
          - A string consisting of 'properties/' followed by a number
        credentials: Optional override for the credentials used to call the
          Analytics Admin API. Provide a google.auth.credentials.Credentials
          instance, a mapping/dict with service account JSON, a JSON string, or
          a path to a service account key file.
    """
    client = create_admin_api_client(credentials_override=credentials)
    request = admin_v1beta.GetPropertyRequest(
        name=construct_property_rn(property_id)
    )
    response = await client.get_property(request=request)
    return proto_to_dict(response)


@mcp.tool(title="Gets property annotations for a property")
async def list_property_annotations(
    property_id: int | str, credentials: CredentialsLike = None
) -> List[Dict[str, Any]]:
    """Returns annotations for a property.

    Annotations are a feature that allows you to leave notes on GA4 for specific dates or periods.
    They are typically used to record service releases, marketing campaign launches or changes,
    and rapid traffic increases or decreases due to external factors.

    Args:
        property_id: The Google Analytics property ID. Accepted formats are:
          - A number
          - A string consisting of 'properties/' followed by a number
        credentials: Optional override for the credentials used to call the
          Analytics Admin API (alpha). Provide a
          google.auth.credentials.Credentials instance, a mapping/dict with
          service account JSON, a JSON string, or a path to a service account
          key file.
    """
    request = admin_v1alpha.ListReportingDataAnnotationsRequest(
        parent=construct_property_rn(property_id)
    )
    annotations_pager = (
        await create_admin_alpha_api_client(
            credentials_override=credentials
        ).list_reporting_data_annotations(request=request)
    )
    all_pages = [
        proto_to_dict(annotation_page)
        async for annotation_page in annotations_pager
    ]
    return all_pages
