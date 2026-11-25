# How to contribute

Read the full [CONTRIBUTING.md](https://github.com/shcglv/patchguard-android-patches/blob/dev/CONTRIBUTING.md) before opening a pull request.

## Quick rules

- Do not submit APKs, DEX files, native libraries, or decompiled application code.
- Do not submit third-party patch code without a compatible license and full attribution.
- Do not claim runtime testing that was not performed.
- Use `dev` as the target branch.
- Use semantic commit messages.
- Sign off your commits with `git commit -s`.
- Do not edit generated files.

## Suggest a source

Open a **Source / patch suggestion** issue with:

- Public GitHub/GitLab URL.
- Exact commit or release tag.
- App name and package name.
- Patch name and purpose.
- License and author, if known.
- Any concerns.

## Contribute documentation or tooling

Focused pull requests with tests are welcome. Run:

```bash
python -m pytest
patchguard validate
```

## Contribute patch code

Patch code is accepted only with clear provenance, a compatible license, and a design that can be reviewed statically. Critical applications are not eligible for distribution.

## Review and merge

All changes go through a pull request and CI. The maintainer may request changes or reject a contribution. Security-sensitive changes may move to a private discussion.
