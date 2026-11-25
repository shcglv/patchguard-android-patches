# Analytics and tracking exclusions — 2026-11-25

Initial static intake of:

- X: [xob0t/morphe-patches](https://github.com/xob0t/morphe-patches/tree/b88dbe8c8bc8517005a7308865fd92023b6a2358) @ `b88dbe8c8bc8517005a7308865fd92023b6a2358`
- B: [Basil-AS/ru-apps-patches](https://github.com/Basil-AS/ru-apps-patches/tree/942c2ac926673db3c49c1a581ed3a9891e47023c) @ `942c2ac926673db3c49c1a581ed3a9891e47023c`
- J: [Jl4cTuk/morphe-patches](https://github.com/Jl4cTuk/morphe-patches/tree/8670317938ee76d0968fde57379ff57b52a79f69) @ `8670317938ee76d0968fde57379ff57b52a79f69`

Status: `EXCLUDE_ANALYTICS_ONLY`. These patches are not part of the suitable catalog or the PatchGuard bundle. All are static-only classifications; no runtime testing was performed.

**Totals:** 33 patch entries / 20 canonical functions: 27 pure analytics/telemetry entries and 6 advertising-ID/ad-pixel tracking-only entries.

The three multi-app B entries each cover 29 packages and together account for 87 app rows.

| # | Function | Entries / apps | Evidence | Why excluded |
|---|---|---|---|---|
| 1 | Adjust | X universal; B universal | X `app/privacy/patches/analytics/DisableAdjustPatch.kt:9`; B `:10` — removes `com.adjust.*` permissions/components | Attribution SDK only |
| 2 | AppMetrica | X universal | `DisableAppMetricaPatch.kt:43` — stubs SDK entry points and manifest | Analytics SDK only |
| 3 | AppsFlyer | X universal; B multi-app 29 packages | X `DisableAppsFlyerPatch.kt:9` (manifest); B `:52` (SDK `start()` + manifest) | Attribution/tracking only |
| 4 | Firebase telemetry | X + B universal | X `DisableFirebaseTelemetryPatch.kt:9`; B `:10` — collection flags and DataTransport components | Telemetry only |
| 5 | Google Analytics | X + B universal | X `DisableGoogleAnalyticsPatch.kt:9`; B `:10` — metadata and GMS analytics/TagManager components | Analytics only |
| 6 | MyTracker | X universal | `DisableMyTrackerPatch.kt:9`; B folds into analytics dependency | Analytics only |
| 7 | RuStore metrics | X + B universal | X `DisableRuStoreMetricsPatch.kt:9`; B `:10` | Metrics only |
| 8 | Sentry telemetry | X + B universal | X `DisableSentryTelemetryPatch.kt:13`; B `:14` — auto-init off, DSN cleared | Telemetry only |
| 9 | Avito telemetry | X + B app-specific | X `app/avito/patches/privacy/DisableTelemetryPatch.kt:10`; B `app/ru_apps/avito/privacy/DisableTelemetryPatch.kt:21` | Clickstream + Adjust + AppMetrica/Varioqub only |
| 10 | Analytics libraries | B multi-app 29 packages | `app/privacy/patches/analytics/jl4ctuk/DisableAnalyticsDependency.kt:444` | AppMetrica/MyTracker/Firebase runtime only |
| 11 | Analytics manifest components | B multi-app 29 packages | Same file `:321` | Manifest analytics components only |
| 12 | Segment analytics | B RuTube | `app/ru_apps/rutube/privacy/DisableSegmentAnalyticsPatch.kt:43` | Event analytics only |
| 13 | OpenTelemetry APM | B VK Video | `app/ru_apps/vkvideo/Patches.kt:634` | Tracing/APM only |
| 14 | RuStore analytics | B RuStore; J RuStore | B `rustore_jl4ctuk/analytics/DisableAnalyticsPatch.kt:109`; J `:111` | AltCraft/MyTracker/OK Tracer/WorkManager analytics only |
| 15 | Ozon telemetry | B Ozon; J Ozon | B `ozon_jl4ctuk/telemetry/DisableOzonTelemetryPatch.kt:164`; J `:164` | Analytics/attribution/crash/upload only |
| 16 | TBank telemetry worker | B T-Bank | `app/ru_apps/tbank/DisableTelemetryWorkerPatch.kt:41` | OpenTelemetry worker only |
| 17 | MAX background telemetry | B MAX | `app/ru_apps/max/DisableBackgroundTelemetryWorkersPatch.kt:41` | apptracer.ru upload + daily permission analytics |
| 18 | Spoof VPN telemetry field | B universal | `app/privacy/patches/vpn/SpoofVpnTelemetryFieldPatch.kt:107` | Alters only telemetry sink values |
| 19 | Advertising ID removal | B MAX, Ozon Bank, RuTube, Sberbank, VK Video | `max/DisableAdvertisingIdPatch.kt:20`; `ozonbank/ads/DisableAdvertisingIdPatch.kt:23`; `rutube/ads/DisableAdvertisingIdPatch.kt:21`; `sberbank/DisableAdvertisingIdPatch.kt:26`; `vkvideo/ResourcePatches.kt:16` | Removes `AD_ID`/`ACCESS_ADSERVICES_*`; tracking-only, no ad removal |
| 20 | Ad pixel tracking | B VK Video | `app/ru_apps/vkvideo/Patches.kt:653` | Stops `PixelStatsTrackerImpl`; measurement only |

## Notes

- `Disable VK Video MyTarget SDK` is **not** in this list: it disables an ad SDK, not analytics, and remains an advertising candidate.
- `Disable ad-free subscription promo` is an advertising/promo patch, not analytics, and remains a candidate.
- `Disable invasive permissions` and `Disable background hooks` are privacy/functional patches, not analytics-only; they are `REVIEW_REQUIRED`.
- If the owner decides that advertising-ID removal counts as a separate privacy feature rather than tracking-only, entries 19 can be moved to review. The current classification is deliberately conservative.
