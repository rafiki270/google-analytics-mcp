# Analytics MCP Expansion Guide

This guide outlines how to extend the Google Analytics MCP server to cover the additional read-only endpoints captured in `Docs/google-api.md`. The goal is to keep the server MCP-compatible while exposing richer Admin and Data API capabilities for all tenants.

## Prerequisites
- **Python ≥ 3.10** (matches `pyproject.toml`).
- Dependencies installed inside a virtual environment (`python -m pip install .`).
- Service-account or user credentials with the required scopes (`analytics.readonly`, plus any product-specific scopes—for example, DV360 requires additional authorisation).
- Updated server with per-request credential overrides (already implemented via the `credentials` parameter in each tool).

## Implementation Approach
- [ ] **Identify the target API surface**  
   Cross-reference the endpoint list in `Docs/google-api.md`. Group work by feature area (e.g., property inventory vs. reporting extensions) so tooling remains modular.

- [ ] **Create or extend tool modules**  
   - Continue using the pattern in `analytics_mcp/tools/...`.  
   - For Admin API additions, extend `analytics_mcp/tools/admin/`. Split large domains (e.g., “links” or “settings”) into dedicated modules if the file grows beyond ~300 lines.  
   - For Data API reporting helpers, add modules under `analytics_mcp/tools/reporting/` (e.g., `pivot.py`, `cohorts.py`, `funnels.py`, `quota.py`).

- [ ] **Define MCP tools**  
   - Use `@mcp.tool()` decorators (or `mcp.add_tool`) mirroring the existing style.  
   - Surface input arguments that map cleanly to the underlying protobuf/REST request. Document defaults and allowable values in docstrings because LLM tool descriptions will surface those details.

- [ ] **Wire credentials**  
   - Every tool should accept `credentials: utils.CredentialsLike = None` and pass it to the relevant client factory (`create_admin_api_client`, `create_data_api_client`, etc.).  
   - For niche services (e.g., DV360, SA360), verify if additional scopes or client libraries are required; update `utils.py` accordingly.

- [ ] **Add tests**  
   - Unit-test helper functions (similar to `tests/utils_test.py`).  
   - Use `unittest.mock` to validate that request objects are constructed correctly and that credential overrides propagate.  
   - If the behaviour is complex, add integration-style tests guarded by environment variables so they can be skipped in CI.

- [ ] **Document usage**  
   - Update `README.md` with new tool descriptions and environment requirements.  
   - Keep `Docs/google-api.md` in sync with implementation progress.

## Suggested Feature Roadmap
Below are example tool ideas aligned with the research. Tackle them in manageable batches.

### Property Inventory & Links
- [ ] `list_data_streams(property_id, credentials=None)`  
- [ ] `get_measurement_protocol_secrets(data_stream_id, credentials=None)`  
- [ ] `list_bigquery_links(property_id, credentials=None)`  
- [ ] `list_display_video360_link_proposals(property_id, credentials=None)`  
- [ ] `list_search_ads360_links(property_id, credentials=None)`  
- [ ] `list_expanded_data_sets(property_id, credentials=None)`  
- [ ] `list_event_create_rules(data_stream_id, credentials=None)`  
- [ ] `list_adsense_links(property_id, credentials=None)`

### Settings & Diagnostics
- [ ] `get_attribution_settings(property_id, credentials=None)`  
- [ ] `get_data_retention_settings(property_id, credentials=None)`  
- [ ] `get_google_signals_settings(property_id, credentials=None)`  
- [ ] `get_property_quota(property_id, credentials=None)`  
- [ ] `run_access_report(property_id_or_account, dimensions, metrics, credentials=None)` (include GA360 warnings)

### Audience & Configuration Entities
- [ ] `list_audiences(property_id, credentials=None)` (with pagination helpers)  
- [ ] `list_channel_groups(property_id, credentials=None)`  
- [ ] `list_custom_dimensions(property_id, credentials=None)` / `list_custom_metrics`  
- [ ] `list_calculated_metrics(property_id, credentials=None)`  
- [ ] `list_key_events(property_id, credentials=None)`

### Data API Reporting Extensions
- [ ] `run_pivot_report(property_id, request_body, credentials=None)`  
- [ ] `run_cohort_report(property_id, request_body, credentials=None)`  
- [ ] `run_funnel_report(property_id, request_body, credentials=None)`  
- [ ] `create_report_task(property_id, sampling_config, credentials=None)` (preview)  
- [ ] `check_compatibility(property_id, dimensions, metrics, credentials=None)`  
- [ ] `get_metadata(property_id, credentials=None)`  
- [ ] `get_property_quotas_snapshot(property_id, credentials=None)`

### Audience & User Activity
- [ ] `search_user_activity(property_id, user_identifier, date_range, credentials=None)` (GA360-only; guard with warnings)  
- [ ] `list_audience_exports(property_id, credentials=None)` / `get_audience_export`  
- [ ] `list_audience_lists(property_id, credentials=None)` (preview)  
- [ ] `run_access_report` (account-level variant) for compliance visibility.

## Development Tips
- **Consistency**: Follow existing naming conventions and docstring style for MCP tools.  
- **Pagination**: Most Admin API list calls return async pagers—use async list comprehensions to gather full responses, just like existing tools.  
- **Error messaging**: Wrap API errors with informative `RuntimeError` messages so LLM clients can relay actionable information.  
- **Rate limits**: Consider adding helper tools that surface quota snapshots before running heavy reports.  
- **Security**: Remind consumers that credentials should be scoped to the minimum necessary permissions; per-request overrides make multitenancy viable without sharing ADC.

Use this document as a roadmap. As new release notes arrive, append additional feature ideas and keep both doc files synchronized.
