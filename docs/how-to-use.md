# How to use PatchGuard

PatchGuard has two parts:

1. A **public catalog and audit archive** that you can read immediately.
2. An **optional Morphe-compatible patch bundle** that becomes usable only after a release exists.

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

Only do this after the repository has published a release with:

- A `.mpp` asset.
- A valid root `patches-bundle.json`.
- A `patches-list.json`.
- Optionally, a signature and public key.

Then add the repository URL in Morphe Manager:

```text
https://github.com/shcglv/patchguard-android-patches
```

PatchGuard does not currently claim that its bundle works on any target app. The repository publishes patches under a static-only review model; read each patch card before using it.

!!! warning
    Only add patch sources you trust. A patch source decides what ends up inside your patched apps. PatchGuard's static review is evidence, not a guarantee.

## Verify a release

If a release exists:

1. Download the `.mpp` asset from the release page.
2. Compare its SHA-256 with the value recorded in `catalog/releases/`.
3. If the release is signed, verify the public key fingerprint shown by Morphe Manager.
4. Read the release notes and the relevant patch card.

Do not install a patched app if the signature or hash does not match.

## What PatchGuard cannot tell you

- Whether a patch applies to your app version.
- Whether the patched app will start or behave correctly.
- Whether the patch is safe at runtime.
- Whether a third-party patch is compatible with your device.

Those questions require runtime testing, which this project does not perform.
