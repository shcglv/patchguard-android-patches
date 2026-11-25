# Statuses

PatchGuard separates **audit status** from **distribution status**. A patch can be statically reviewed and still not be approved for distribution.

## Audit statuses

| Status | Meaning | Runtime tested |
|---|---|---|
| `DISCOVERED` | A source or patch was recorded; no review yet. | No |
| `PENDING` | Queued for static review. | No |
| `STATIC_AUDITING` | Static review is in progress. | No |
| `STATICALLY_REVIEWED` | The planned static checks for a specific source revision are complete; limitations are documented. | No |
| `UNVERIFIED` | Not enough source, metadata, license or provenance data for a meaningful review. | No |
| `REJECTED` | The patch failed review or policy. | No |
| `BLOCKED` | A critical finding, critical-app policy, or license/security prohibition prevents distribution. | No |
| `UPDATE_AVAILABLE` | The upstream source changed and a new static review is required. | No |
| `OUTDATED` | The reviewed revision no longer matches current app or source versions. | No |

`STATICALLY_REVIEWED` is not a safety guarantee. It means “the static process was completed for this exact revision”, with the stated coverage and limitations.

## Distribution statuses

| Status | Meaning |
|---|---|
| `NOT_ELIGIBLE` | External patch; PatchGuard does not distribute it. |
| `CANDIDATE` | PatchGuard's own patch, a candidate for distribution. |
| `APPROVED` | The owner explicitly approved distribution in a decision record. |
| `BLOCKED` | Distribution is prohibited by policy or a critical finding. |

`APPROVED` is never automatic. It requires a decision record with the approver, date, reason, evidence and scope. It does not imply runtime verification.

## Compatibility labels

| Label | Meaning |
|---|---|
| `DECLARED` | The patch author declares compatibility in metadata. PatchGuard has not independently assessed it. |
| `STATICALLY_ASSESSED` | PatchGuard reviewed the declared versions, fingerprints, version gates and metadata. No runtime test was performed. |
| `NOT_RUNTIME_TESTED` | Always true in the current model. The patch was not run against the app. |

## Freshness labels

| Label | Meaning |
|---|---|
| `CURRENT` | Checked and no relevant upstream change. |
| `UPDATE_AVAILABLE` | A newer upstream revision or release exists. |
| `REVIEW_REQUIRED` | Changes affect the patch or its dependencies; a new static review is required. |
| `STALE` | Not checked within the configured period (default 90 days). |
| `SOURCE_UNAVAILABLE` | The repository or release is unreachable. |
| `ARCHIVED` | The upstream repository is archived. |
| `UNKNOWN` | Freshness could not be determined. |

## Transition rules

The allowed transitions are defined in `config/status_transitions.yml`. In general:

- A new revision never inherits the previous revision's status automatically.
- `BLOCKED` is terminal for distribution unless the owner records a policy exception.
- `REJECTED` can return to `PENDING` only with a new review.
- `APPROVED` can be withdrawn or blocked, but the decision history is retained.
