# Internal runbooks

This directory contains maintainer-facing runbooks. Public project documentation is in English; internal operational notes may be in Russian for the owner's convenience.

## Rules

- Never place secret values, tokens, private keys, or personal data here.
- Reference secrets by name only (for example `MORPHE_SIGNING_KEY`), not by value.
- Record exact commands, expected results, rollback steps and evidence paths.
- Update the runbook after every incident or process change.

## Runbooks

- `runbooks/bootstrap.md` — Stage 0 status, repository creation, settings, release gate (exists).
- `runbooks/release.md` — static gate, signing, release verification (planned).
- `runbooks/update-check.md` — weekly source checks and re-audit queue (planned).
- `runbooks/key-rotation.md` — signing key rotation and user communication (planned).
- `runbooks/incident.md` — compromised key, artifact, or catalog record (planned).
- `runbooks/community-submission.md` — preflight, application text, submission record (planned).

Runbooks are added when the corresponding process is implemented; empty placeholder files are intentionally avoided.
