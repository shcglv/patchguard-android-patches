# How to use PatchGuard

PatchGuard has two parts:

1. A **public catalog and audit archive** that you can read immediately.
2. A **Morphe-compatible patch bundle**. Version `v1.0.0` is published and can be
   added to Morphe Manager.

## Read the catalog

Start with:

- `catalog/` — machine-readable records.
- `audits/records/` — static audit reports and findings.
- `docs/catalog/` — generated human-readable pages.

Every patch card states:

- The audit status and date.
- The exact source commit and SHA-256.
- The compatibility basis (`DECLARED`, `STATICALLY_ASSESSED`, `NOT_RUNTIME_TESTED`).
- What was reviewed and what was not.

## Add the patch source to Morphe Manager

Open the deep link:

<https://morphe.software/add-source?github=shcglv/patchguard-android-patches>

Or add the repository manually in **Morphe Manager → Sources → + → Remote**:

```text
https://github.com/shcglv/patchguard-android-patches
```

The `v1.0.0` source publishes three Ozon 19.31.0 UI patches: Disable checkout
tips, Hide seller rating prompt, and Show final prices only. The release is
unsigned; Manager accepts it while no signing key is pinned. No target APK was
patched or launched, so compatibility is declared rather than runtime-verified.

!!! warning
    Only add patch sources you trust. A patch source decides what ends up inside your patched apps. PatchGuard's static review is evidence, not a guarantee.

## Verify the v1.0.0 release

1. Download `patches-1.0.0.mpp` from the [v1.0.0 release](https://github.com/shcglv/patchguard-android-patches/releases/tag/v1.0.0).
2. Compare its SHA-256 with `5976619bf788b07bc3aa95fd412fc834490a213d8568cf0c686b2c9abe2d4db4`.
3. The release is unsigned; if a future release is signed, verify the key fingerprint shown by Morphe Manager.
4. Read the [verification report](https://github.com/shcglv/patchguard-android-patches/blob/main/reports/releases/v1.0.0.md).

Do not install a patched app if the hash does not match.

## What PatchGuard cannot tell you

- Whether a patch applies to your app version.
- Whether the patched app will start or behave correctly.
- Whether the patch is safe at runtime.
- Whether a third-party patch is compatible with your device.

Those questions require runtime testing, which this project does not perform.
