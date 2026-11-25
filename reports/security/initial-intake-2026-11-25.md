# Security review — initial intake, 2026-11-25

Read-only static intake of X/B/J at the pinned commits. No APK, `.mpp`, native library or runtime test was performed. Every item below is **BLOCKED for distribution** through PatchGuard, regardless of whether it is technically functional. Read-only source analysis may continue.

## Security-sensitive functions (21 canonical, 30 entries)

| # | Function | Source and file:line | Risk | Status |
|---|---|---|---|---|
| 1 | Bypass anti-tamper (T-Bank) | X `app/tbank/patches/antitamper/BypassAntiTamperPatch.kt:125`; B `app/ru_apps/tbank/BypassAntiTamperPatch.kt:126` | CRITICAL: stubs native RASP executor and tamper flags | BLOCKED |
| 2 | Bypass RootBeer (Avito, T-Bank, Ozon, Ozon Bank) | B `app/privacy/patches/security/BypassRootBeerPatch.kt:38` | CRITICAL: root detection bypass | BLOCKED |
| 3 | Bypass STCrypt CKey root (T-Bank) | B `app/privacy/patches/security/BypassStCryptRootBeerPatch.kt:56` | CRITICAL: root detection bypass | BLOCKED |
| 4 | Bypass VPN check (MAX) | B `app/ru_apps/max/BypassVpnCheckPatch.kt:33` | HIGH: collapses external IP checker list | BLOCKED |
| 5 | Bypass native signature (VK Video) | B `app/ru_apps/vkvideo/NativeSignaturePatch.kt:38` | CRITICAL: byte-patches `libvkcore.so` signature check | BLOCKED |
| 6 | Disable freeRASP | X `app/privacy/patches/security/DisableFreeRaspPatch.kt:34`; B `:38` | CRITICAL: disables mobile security SDK | BLOCKED |
| 7 | Disable Kaspersky SDK (Sberbank) | B `app/ru_apps/sberbank/DisableKasperskySdkPatch.kt:25` | HIGH: disables antivirus SDK components | BLOCKED |
| 8 | Disable background scan (RuStore) | B `app/ru_apps/rustore_jl4ctuk/kaspersky/DisableKasperskyScanPatch.kt:46`; J `:46` | HIGH: cancels periodic antivirus scan | BLOCKED |
| 9 | Spoof USB debugging | X `app/privacy/patches/usb/SpoofUsbDebuggingStatusPatch.kt:137`; B `:138` | HIGH: anti-detection | BLOCKED |
| 10 | Spoof VPN status | X `app/privacy/patches/vpn/SpoofVpnStatusPatch.kt:196`; B `:200` | HIGH: anti-detection | BLOCKED |
| 11 | Spoof default proxy/DNS | B `app/privacy/patches/vpn/SpoofDefaultProxyAndDnsPatch.kt:55` | HIGH: anti-detection | BLOCKED |
| 12 | Spoof emulator | X `app/privacy/patches/emulator/SpoofEmulatorStatusPatch.kt:216`; B `:217` | HIGH: anti-detection | BLOCKED |
| 13 | Spoof install source | X `app/privacy/patches/installsource/SpoofInstallSourcePatch.kt:46`; B `:47` | HIGH: installer spoof | BLOCKED |
| 14 | Spoof installed VPN apps | B `app/privacy/patches/vpn/SpoofInstalledVpnAppsPatch.kt:62` | HIGH: hides VPN clients | BLOCKED |
| 15 | Spoof network MTU | B `app/privacy/patches/vpn/SpoofNetworkInterfaceMtuPatch.kt:59` | HIGH: tunnel detection | BLOCKED |
| 16 | Spoof system proxy | B `app/privacy/patches/vpn/SpoofProxyDetectionPatch.kt:64` | HIGH: anti-detection | BLOCKED |
| 17 | Replace RuStore device identifier | B `app/ru_apps/rustore/FeaturePatches.kt:26` | CRITICAL: zero UUID in payment/session requests | BLOCKED |
| 18 | Replace VK device identifier | B `app/ru_apps/rustore/FeaturePatches.kt:45` | CRITICAL: zero UUID in VK ID/Pay paths | BLOCKED |
| 19 | Restore secure-session compatibility | B `rustore_jl4ctuk/session/RestoreSecureSessionCompatibilityPatch.kt:72`; J `:71` | CRITICAL: patches native `libbridge_helper.so` certificate digest and code bytes | BLOCKED |
| 20 | Skip update authentication | B `rustore_jl4ctuk/auth/DisableVkIdAuthPromptPatch.kt:14`; J `:13` | HIGH: bypasses auth suggestion | BLOCKED |
| 21 | Unlock subscription features | B `app/ru_apps/rutube/subscription/UnlockSubscriptionFeaturesPatch.kt:10` | HIGH: forces paid-subscription flag globally | BLOCKED |

## Critical applications (7)

| Application | Package | Entries | Allowed |
|---|---|---:|---|
| T-Bank | `com.idamob.tinkoff.android` | 10 | read-only source/docs |
| Ozon Bank | `ru.ozon.fintech.finance` | 11 | read-only |
| Sberbank | `ru.sberbankmobile` | 4 | read-only |
| Alfa-Bank | `ru.alfabank.mobile.android` | 3 | read-only |
| VTB Online | `ru.vtb24.mobilebanking.android` | 3 | read-only |
| Mir Pay | `ru.nspk.mirpay` | 3 | read-only |
| Yandex Pay | `com.yandex.bank` | 3 | read-only |

`Remove TBank ads` and the three Ozon Bank UI patches may be cataloged, but they are `BLOCKED` for bundle inclusion and distribution. No build, no install, no runtime test.

## Review-required, not security bypass

| Function | Reason |
|---|---|
| RuStore `Disable invasive permissions` | Removes 12+ permissions and 29 verification components; may break install/update/SMS/QR flows. |
| RuStore `Disable background hooks` | Removes network/boot providers and changes WorkManager behavior; privacy gain but side effects possible. |
| RuTube `Lift download restrictions` | Bypasses local download restrictions; policy-sensitive, not financial. |
| VK Video `Fix install conflict with stock VK` | Removes duplicate signature-permission declarations; needed for re-signed APK, but needs manifest review. |

## Limitations

- Static review only; native byte patches cannot be verified without the target binary, and no binary was downloaded.
- No runtime behavior, compatibility, or anti-tamper/anti-fraud effectiveness was tested.
- The `Restore secure-session` and `Bypass native signature` entries are especially unsafe to approve without independent native-binary review.
