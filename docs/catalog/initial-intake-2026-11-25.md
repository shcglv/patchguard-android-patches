# Initial source intake — 2026-11-25

Read-only static intake of three community patch sources. No APK, `.mpp`, binary archive or decompiled target app was downloaded. No build or runtime test was performed. This is an inventory and triage result, not a full static audit and not an approval.

!!! important
    All three sources are pinned to exact commits. Compatibility and runtime behavior are **not** verified. `CAND` means “worth further static audit”, not “safe” or “working”.

## Sources

| Source | Default branch | HEAD | Latest release | License | Entries | Apps | Universal |
|---|---|---|---|---|---|---:|---:|
| [xob0t/morphe-patches](https://github.com/xob0t/morphe-patches/tree/b88dbe8c8bc8517005a7308865fd92023b6a2358) | `main` | `b88dbe8c8bc8517005a7308865fd92023b6a2358` | `v1.14.19` | GPL-3.0 | 25 | 4 | 13 |
| [Basil-AS/ru-apps-patches](https://github.com/Basil-AS/ru-apps-patches/tree/942c2ac926673db3c49c1a581ed3a9891e47023c) | `main` | `942c2ac926673db3c49c1a581ed3a9891e47023c` | `v1.4.0` | GPL-3.0 | 90 | 32 groups / 30 packages | 16 |
| [Jl4cTuk/morphe-patches](https://github.com/Jl4cTuk/morphe-patches/tree/8670317938ee76d0968fde57379ff57b52a79f69) | `main` | `8670317938ee76d0968fde57379ff57b52a79f69` | `v1.4.0` | GPL-3.0 | 24 | 3 | 0 |

Basil HEAD is 27 minutes newer than its `v1.4.0` release; the exact release commit is still to be verified. `patches-list.json` at HEAD reports version `1.4.0`.

**Collective:** 30 unique package names, 29 real applications + 1 Example, 139 patch entries, 110 distinct normalized implementations, 176 real app/universal rows for Basil (excluding Example).

## Applications

`TBank`/`T-Bank` and `Sberbank`/`СберБанк` were merged by package name. `Ozon` and `Ozon Bank` are separate. No application has an unknown package name.

| Application | Package | Sources | Entries | Supported versions | Suitable candidates | Critical |
|---|---|---|---|---:|---|---|
| Avito | `com.avito.android` | X, B | 20 | 229.1–238.0 (16) | 7 | no |
| T-Bank | `com.idamob.tinkoff.android` | X, B | 10 | 7.39.0–8.7.1 (11) | 0* | **yes** |
| Wildberries | `com.wildberries.ru` | X, B | 5 | 7.7.2001–7.9.0000 (36) | 1 | no |
| Ozon | `ru.ozon.app.android` | X, B, J | 24 | 19.27.0–19.45.0 (21) | 8 | no |
| Ozon Bank | `ru.ozon.fintech.finance` | B, J | 11 | 19.31.0, 19.37.0 | 0* | **yes** |
| RuStore | `ru.vk.store` | B, J | 28 | 1.108.0.2–1.111.0.3 (3) | 6 + 2 review | no |
| VK Video | `com.vk.vkvideo` | B | 21 | 1.163, 1.165 | 13 + 1 review | no |
| RuTube | `ru.rutube.app` | B | 10 | 31.14.2, 31.17.2 | 3 + 1 review | no |
| MAX | `ru.oneme.app` | B | 6 | 26.10.1–26.35.0 (4) | 0 | no |
| Sberbank | `ru.sberbankmobile` | B | 4 | 17.13.0 | 0* | **yes** |
| Alfa-Bank | `ru.alfabank.mobile.android` | B | 3 | 12.60.07 | 0* | **yes** |
| VTB Online | `ru.vtb24.mobilebanking.android` | B | 3 | 20.18.1.3 | 0* | **yes** |
| Mir Pay | `ru.nspk.mirpay` | B | 3 | 1.64.5.350 | 0* | **yes** |
| Yandex Pay | `com.yandex.bank` | B | 3 | 0.243.0 | 0* | **yes** |
| 2GIS | `ru.dublgis.dgismobile` | B | 3 | 7.29.1.632.4 | 0 | no |
| AliExpress | `ru.aliexpress.buyer` | B | 3 | 8.89.1.3597464 | 0 | no |
| Beeline | `ru.beeline.services` | B | 3 | 5.48.5 | 0 | no |
| Gosuslugi | `ru.rostel` | B | 3 | 27.1.0.9876-rustore | 0 | no (high sensitivity) |
| MTS | `ru.mts.mymts` | B | 3 | 6.77 | 0 | no |
| MegaFon | `ru.megafon.mlk` | B | 3 | 4.69.0 | 0 | no |
| Perekrestok | `ru.perekrestok.app` | B | 3 | 3.99.0 | 0 | no |
| Whoosh | `com.punicapp.whoosh` | B | 3 | 4.0.0 | 0 | no |
| Yandex Go | `ru.yandex.taxi` | B | 3 | 5.98.0 | 0 | no |
| Yandex Mail | `ru.yandex.mail` | B | 3 | 9.30.1 | 0 | no |
| Yandex Maps | `ru.yandex.yandexmaps` | B | 3 | 31.1.3 | 0 | no |
| Yandex Music | `ru.yandex.music` | B | 3 | 2026.09.5 #167.1rur | 0 | no |
| Yandex Rasp | `ru.yandex.rasp` | B | 3 | 3.73.0 | 0 | no |
| Yandex Weather | `ru.yandex.weatherplugin` | B | 3 | 26.10.10 | 0 | no |
| Zvuk | `com.zvooq.openplay` | B | 3 | 4.117.0rs | 0 | no |
| XYZ app | `com.example.app` | B | 1 | 1.0.2, 2.0.0 | 0 (Example) | — |

`*` — functional patches exist but the application is CRITICAL: read-only analysis only, never bundle distribution.

Nineteen applications have only the three shared analytics-only patches. MAX, Sberbank and the six financial applications have no distribution-eligible candidate. Only six applications have suitable functions.

## Patch classification

| Class | Entries | Canonical functions |
|---|---:|---:|
| Suitable candidates (`CAND` / `CAND-R`) | 67 | **42** (38 + 4 review) |
| Analytics/tracking-only (`EXCLUDE_ANALYTICS_ONLY`) | 33 | 20 |
| Security-sensitive (`BLOCKED`) | 30 | 21 |
| Critical-app functional (`BLOCKED`) | 8 | 4 |
| Example (`EX`) | 1 | 1 |
| **Total** | **139** | **110** |

### Universal patches

- X: 13 — 8 analytics-only, 5 security/anti-detection.
- B: 16 — 6 analytics-only, 10 security/anti-detection.
- J: 0.

No universal patch is suitable for distribution. Ten X/B universal implementations are exact-identical (5 analytics, freeRASP, 4 spoofs). The shared B analytics bundle covers 29 packages with 3 entries (87 app rows).

## Duplicates and competing implementations

- **28 exact cross-repository groups** + **1 same-source duplicate** (`Remove Ozon ads` appears twice in B with the same normalized hash).
- **16 competing groups** where the same app/function has different implementations.
- 14 identical B↔J groups; 14 identical X↔B groups (10 universal + 4 app-specific).

Key competing decisions:

| App | Function | Recommendation |
|---|---|---|
| Avito | Remove ads | X base; port B's Yandex SDK class fix. 98% normalized similarity. |
| Avito | Block listings | X (dynamic item-binder discovery); B is fixed-class simplification. |
| Avito | Hide professional sellers | B (multi-return hooks); X single hook. |
| Avito | Morphe settings | X (multiple return points); B single last return. |
| Avito | UI tweaks | X base + B ProfilePro filters. |
| Wildberries | Remove Wildberries ads | X (more complete suspend/Flow/empty-flow logic). |
| Ozon | Remove Ozon ads | J for 19.31 (checkout/floating/marketing widgets); X for legacy 19.27–19.45; do not merge blindly. |
| Ozon | Lottery / account feed | J (extra Morkovsk onboarding and EntryBanner mappers). |
| Ozon Bank | VPN warning | J clean; B adds analytics dependency. Critical app: catalog only. |
| RuStore | Mine / gaming | B (graceful `methodOrNull` / `matchOrNull`). |
| RuStore | Background scan | J more elaborate; security-sensitive, blocked. |

Full exclusion log: [analytics-2026-11-25.md](https://github.com/shcglv/patchguard-android-patches/blob/dev/audits/exclusions/analytics-2026-11-25.md).

Full security review: [initial-intake-2026-11-25.md](https://github.com/shcglv/patchguard-android-patches/blob/dev/reports/security/initial-intake-2026-11-25.md).

## Merge recommendations

| App | Base | Notes |
|---|---|---|
| Avito | X | Port B robustness fixes; combine UI tweaks and ProfilePro; reject analytics/RootBeer. |
| Ozon | J for 19.31; X legacy | Keep two ads variants by version; J for UI; reject analytics/RootBeer. |
| Wildberries | X | Compare B before merge; reject analytics. |
| RuStore | B + J `Restrict background work` | Keep 6 clean + 2 review; block 5 security-sensitive; reject analytics. |
| RuTube | B | 3 clean + 1 review; block subscription unlock. |
| VK Video | B | 12 ad layers are complementary; merge into one optioned patch after conflict map; block native signature; reject analytics. |
| T-Bank / Ozon Bank | — | No merge for distribution; read-only catalog. |
| Other apps | — | Shared analytics bundle only; no suitable functions. |

No physically merged source code was produced.

## Candidate catalog (42)

`CAND` = suitable candidate; `CAND-R` = review required. Not approved and not runtime-tested.

| # | App | Patch | Preferred source |
|---|---|---|---|
| A1 | Avito | AMOLED dark theme | X (identical B) |
| A2 | Avito | Block listings | X |
| A3 | Avito | Disable update prompts | X (identical B) |
| A4 | Avito | Hide professional sellers | B |
| A5 | Avito | Morphe settings | X |
| A6 | Avito | Remove ads | X + B fix |
| A7 | Avito | UI tweaks | X + B ProfilePro |
| O1 | Ozon | Remove Ozon ads | J / X legacy |
| O2 | Ozon | Disable checkout tips | J/B |
| O3 | Ozon | Disable lottery and in-app pushes | J |
| O4 | Ozon | Disable tip notifications | J/B |
| O5 | Ozon | Hide Ozon Bank ad banner | J/B |
| O6 | Ozon | Hide account lottery and review feed | J |
| O7 | Ozon | Hide seller rating prompt | J/B |
| O8 | Ozon | Show final prices only | J/B |
| W1 | Wildberries | Remove Wildberries ads | X |
| R1 | RuStore | Disable ads | B/J |
| R2 | RuStore | Disable Mine redesign | B |
| R3 | RuStore | Disable gaming profile | B |
| R4 | RuStore | Disable push services | B/J |
| R5 | RuStore | Exclude Google Play apps from updates | B/J |
| R6 | RuStore | Restrict background work to updates | J |
| R7 | RuStore | Disable background hooks | B/J (`CAND-R`) |
| R8 | RuStore | Disable invasive permissions | B/J (`CAND-R`) |
| T1 | RuTube | Disable ads | B |
| T2 | RuTube | Enable background playback | B |
| T3 | RuTube | Custom branding icon | B |
| T4 | RuTube | Lift download restrictions | B (`CAND-R`) |
| V1 | VK Video | Block deep midroll ads | B |
| V2 | VK Video | Block midroll ads | B |
| V3 | VK Video | Disable VK Video MyTarget SDK | B |
| V4 | VK Video | Disable video ad repository | B |
| V5 | VK Video | Filter Clips SDK ads | B |
| V6 | VK Video | Filter clip feed ads | B |
| V7 | VK Video | Hide ad XML surfaces | B |
| V8 | VK Video | Hide home showcase ads | B |
| V9 | VK Video | Hide promoted banner content | B |
| V10 | VK Video | Remove clip ads | B |
| V11 | VK Video | Remove video ads | B |
| V12 | VK Video | Disable ad-free subscription promo | B |
| V13 | VK Video | Disable in-app update | B |
| V14 | VK Video | Fix install conflict with stock VK | B (`CAND-R`) |

## Counts

1. Applications: **29 real + 1 Example** (30 packages; 32 groups before merge).
2. Patch entries: **139**; distinct normalized implementations: **110**.
3. Exact duplicates: **28 cross-repo groups + 1 same-source**; competing groups: **16**.
4. Analytics/tracking-only excluded: **33 entries / 20 functions**.
5. Security-sensitive: **30 entries / 21 functions**, all blocked for distribution.
6. Further suitable candidates: **42** (38 clean + 4 review).
7. Critical applications: **7**.
8. Recommended merge families: **6** (Avito, Ozon, Wildberries, RuStore, RuTube, VK Video).
9. Unresolved: exact Basil release commit; Ozon ads version split; ad-ID classification; `Disable VK Video MyTarget SDK` classification; VK composite design; policy for lift-download/unlock; RuStore permission side effects; native/secure-session review; GPL attribution before merge; no runtime verification.

## Limitations

- No target APK, `.mpp`, native library, decompilation, build or runtime test.
- Full line-by-line audit was not performed; this is intake/triage. No patch is `STATICALLY_REVIEWED`.
- One Java extension file (`BlacklistActivity.java`, Avito Block listings) timed out during the first fetch and is `NOT_REVIEWED`; the Kotlin part was read.
- `patches-list.json` is generated and may omit unpublished/experimental source blocks.
- All sources are GPL-3.0 with the Morphe 7c NOTICE; B contains explicit “Ported from xob0t/Jl4cTuk” attribution comments. Any future merge must preserve those notices and attribution.
