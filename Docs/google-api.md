# Google Analytics API Reference (Read-Only Surfaces)

> Last updated: 2025-01 (manual review + Gemini cross-check).  
> If you need newer details, consult the official Google Analytics Admin/Data API release notes.

This reference lists important read-only Google Analytics endpoints that the MCP server does **not** implement yet. Use it when planning new tooling. Links point to the canonical REST documentation; the corresponding Python client lives under `google.analytics.admin_v1beta` (or `admin_v1alpha`) and `google.analytics.data_v1beta`.

## Admin API

### Property Configuration & Inventory
- **Data Streams**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataStreams  
  - Python: `AnalyticsAdminServiceAsyncClient.list_data_streams`, `.get_data_stream`
- **Measurement Protocol Secrets** (per web/app stream)  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataStreams.measurementProtocolSecrets  
  - Python: `.list_measurement_protocol_secrets`, `.get_measurement_protocol_secret`
- **Firebase Links**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.firebaseLinks  
  - Python: `.list_firebase_links`
- **Google Ads / DV360 / SA360 Links** (beyond the Ads list already exposed)  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.googleAdsLinks  
  - Python: `.list_google_ads_links`
- **Display & Video 360 Link Proposals**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.displayVideo360AdvertiserLinkProposals  
  - Python: `.list_display_video360_advertiser_link_proposals`
- **Search Ads 360 Links**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.searchAds360Links  
  - Python: `.list_search_ads360_links`
- **BigQuery Links**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.bigQueryLinks  
  - Python: `.list_big_query_links`
- **Expanded Data Sets**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.expandedDataSets  
  - Python: `.list_expanded_data_sets`, `.get_expanded_data_set`
- **Event Create Rules**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataStreams.eventCreateRules  
  - Python: `.list_event_create_rules`
- **AdSense Links**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.adSenseLinks  
  - Python: `.list_ad_sense_links`
- **Roll-up / Subproperty settings**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.rollupProperty  
  - Python: `.get_rollup_property_source_links`, `.list_subproperty_event_filters`
- **Subproperty Sync Configuration**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.subpropertyEventFilters  
  - Python: `.get_subproperty_event_filter`, `.list_subproperty_event_filters`
- **Key Events**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.keyEvents  
  - Python: `.list_key_events`, `.get_key_event`

### Audiences, Channel Groups & Other Entities
- **Audiences**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.audiences  
  - Python: `.list_audiences`, `.get_audience`
- **Channel Groups**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.channelGroups  
  - Python: `.list_channel_groups`, `.get_channel_group`
- **Conversion Events**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.conversionEvents  
  - Python: `.list_conversion_events`
- **Custom Dimensions & Metrics (configuration)**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.customDimensions  
  - Python: `.list_custom_dimensions`, `.list_custom_metrics`
- **Calculated Metrics** (beta)  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.calculatedMetrics  
  - Python: `.list_calculated_metrics`

### Access, Users & Diagnostics
- **Access Bindings / User Links**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.userLinks  
  - Python: `.list_user_links`, `.audit_user_links`
- **Access & Usage Reports**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accounts.accessReports and .../properties.accessReports  
  - Python: `.query_access_bindings`, `.run_access_report` (available on both account and property clients)  
  > Non-quota dimensions require GA360 and an Administrator role.
- **Change History**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/accountSummaries/changeHistoryEvents  
  - Python: `.search_change_history_events`
- **Enhanced Measurement Settings**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataStreams.enhancedMeasurementSettings  
  - Python: `.get_enhanced_measurement_settings`
- **SKAdNetwork Conversion Value Schemas**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataStreams.sKAdNetworkConversionValueSchemas  
  - Python: `.list_ska_d_network_conversion_value_schemas`
- **Attribution Settings**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.attributionSettings  
  - Python: `.get_attribution_settings`
- **Data Retention Settings**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.dataRetentionSettings  
  - Python: `.get_data_retention_settings`
- **Google Signals Settings**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.googleSignalsSettings  
  - Python: `.get_google_signals_settings`
- **Property Quota Snapshot (Admin)**  
  - REST: https://developers.google.com/analytics/devguides/config/admin/v1/rest/v1alpha/properties.propertyQuota  
  - Python: `.get_property_quota`

## Data API

### Core Reporting Extensions
- **Run Pivot Report**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runPivotReport  
  - Python: `BetaAnalyticsDataAsyncClient.run_pivot_report`
- **Run Cohort Report**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runCohortReport  
  - Python: `.run_cohort_report`
- **Run Funnel Report**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runFunnelReport  
  - Python: `.run_funnel_report`
- **Run Funnel Exploration**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/runRealtimeReport#body.FIELDS.funnel  
  - Python: see `FunnelReportRequest` helpers within the client
- **Metadata Compatibility Check**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/checkCompatibility  
  - Python: `.check_compatibility`
- **Property Metadata (Dimensions & Metrics)**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/getMetadata  
  - Python: `.get_metadata`
- **Comparisons in Reports**  
  - REST: `RunReportRequest.comparisons` field  
  - Python: pass `comparisons` when calling `.run_report` or `.run_pivot_report`.
- **Advanced Sampling Control**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/reference/rest/v1beta/properties.reportTasks  
  - Python: `.create_report_task` (preview) supports sampling level selection, including GA360-only options.

### Realtime Enhancements
- **Realtime Metadata**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/getRealtimeMetadata  
  - Python: `BetaAnalyticsDataAsyncClient.get_realtime_metadata`
- **Realtime Details (Breakdowns & Quota)**  
  - Covered partially by existing `run_realtime_report`, but consider exposing helper tools for quota diagnostics: `.run_realtime_report(return_property_quota=True)`

### User Activity & Attribution
- **User Activity API** (privileged access)  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/userActivity:search  
  - Python: `.search_user_activity`  
  > Requires Analytics 360 and special enablement; include safeguards if you expose it.
- **Audience Exports**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/audienceExports  
  - Python: `.list_audience_exports`, `.get_audience_export`
- **Audience Lists (Preview)**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/audienceLists  
  - Python: `.list_audience_lists`, `.get_audience_list` (read-only preview)
- **Attribution Settings / Reporting**  
  - Admin gets configuration; reporting surfaces live in the GA export dataset (BigQuery). No direct Data API endpoint currently exposes attribution summary reports—watch release notes.
- **Property Quotas Snapshot (Data API)**  
  - REST: https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/properties/getPropertyQuotasSnapshot  
  - Python: `.get_property_quotas_snapshot`

## Release Notes & Changelog
- Admin API release notes: https://developers.google.com/analytics/devguides/config/admin/v1/release-notes
- Data API release notes: https://developers.google.com/analytics/devguides/reporting/data/v1/release-notes

Keep an eye on these pages for new beta resources or fields. Whenever either API adds a new surface, update this document so it remains a current reference for MCP tooling work.
