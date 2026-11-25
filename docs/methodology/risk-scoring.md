# Risk scoring

PatchGuard uses a 0–100 heuristic score to summarize static risk. It is **not** a probability of compromise and it does not replace reading the audit report.

## Dimensions

| Dimension | Weight | What it measures |
|---|---|---|
| Provenance | 15 | Author/repository identity, commit consistency, release provenance. |
| Source transparency | 10 | Readable source, no unexplained binaries, clear build scripts. |
| Manifest/permissions | 10 | Permissions and components declared by the patch or extension source. |
| Network (static) | 15 | Network APIs, destinations and data passed in source code. |
| Dependencies | 10 | Provenance, versions, licenses and known vulnerabilities. |
| Code changes | 10 | Size and sensitivity of modifications, dead code, unusual control flow. |
| Security-sensitive | 15 | Authentication, TLS, integrity, tokens, crypto, anti-fraud, accessibility. |
| Static analysis | 10 | Coverage and quality of static checks and manual review. |
| Known vulnerabilities | 5 | Known CVEs affecting the patch or dependencies. |

The weighted total is rounded to an integer from 0 to 100.

## Bands

| Score | Band | Interpretation |
|---|---|---|
| 0–19 | Low | No significant concerns in the reviewed scope; runtime remains unknown. |
| 20–39 | Moderate | Some concerns or missing evidence; read limitations. |
| 40–59 | Elevated | Material concerns; distribution needs explicit owner acceptance. |
| 60–79 | High | Serious concerns; default to rejection unless the owner accepts the risk. |
| 80–100 | Critical | Critical finding or unacceptable policy risk; blocked. |

## Critical findings

Any of the following forces `score = 100` and `BLOCKED`, regardless of the weighted total:

- Data exfiltration.
- Authentication bypass.
- TLS certificate pinning bypass.
- Integrity check bypass.
- Dynamic code loading without a clear, reviewed purpose.
- Hidden or unexplained network destination.
- Credential theft.
- Malicious payload.
- Unauthorized file access.
- Anti-fraud bypass.

## Confidence

Confidence is separate from risk:

- `LOW` — partial source, missing dependencies, unclear license or limited coverage.
- `MEDIUM` — full source, provenance, license, dependencies and static checks completed; runtime still unknown.
- `HIGH` — not used. Runtime behavior is not observed.

## Important limits

- The score is a communication tool, not a mathematical proof.
- A low score does not mean “safe”.
- Missing information can produce a misleadingly low score; such cases should be `UNVERIFIED`, not scored as low risk.
- A high score does not prove malicious intent; it indicates that the evidence warrants caution or rejection.
