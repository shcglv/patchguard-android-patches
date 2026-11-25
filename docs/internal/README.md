# Internal runbooks

This directory contains maintainer-facing runbooks. Public project documentation is in English; internal operational notes may be in Russian for the owner's convenience.

## Rules

- Never place secret values, tokens, private keys, or personal data here.
- Reference secrets by name only (for example `MORPHE_SIGNING_KEY`), not by value.
- Record exact commands, expected results, rollback steps and evidence paths.
- Update the runbook after every incident or process change.

## Planned runbooks

- `bootstrap.md` — repository creation, rulesets, release identity.
- `release.md` — static gate, signing, release verification.
- `update-check.md` — weekly source checks and re-audit queue.
- `key-rotation.md` — signing key rotation and user communication.
- `incident.md` — compromised key, artifact, or catalog record.
- `community-submission.md` — preflight, application text, submission record.

At Stage 0, only this index exists. Runbooks are added when the corresponding process is implemented; empty placeholder files are intentionally avoided.
