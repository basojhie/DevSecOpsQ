# Operations and safe test matrix

| Area | Components | Current automation | Constraint |
|---|---|---|---|
| Asset inventory | Subfinder, dnsx, anew | Passive discovery and delta | Exact approved root domains only |
| HTTP metadata | httpx | Low-rate metadata | No redirect-follow to out-of-scope host |
| URL history | gau | Candidate extraction | Historical URLs are not evidence of a live route |
| Crawling | Katana | Optional staging profile | Depth 2, concurrency 2, request rate 2 |
| Ports/services | Naabu, Nmap | Optional staging profile | Top 100 ports; Nmap only Naabu-derived hosts |
| Content discovery | ffuf | Installed, not executed | Per-target wordlist and separate approval required |
| Vulnerability templates | Nuclei | Not wired as unattended run | Curated reviewed template set only |
| TLS | testssl.sh | Planned | Low-impact schedule and explicit host allowlist |
| DAST | OWASP ZAP | Planned baseline | Authenticated/active scan requires separate staging approval |
| Parameter testing | Dalfox | Planned | Only approved staging URL/parameter cases |
| Source code | Semgrep | Separate PR workflow | Repository contents only |
| Secrets | Gitleaks | Separate PR workflow | Never publish secret values; rotate exposed credentials |
| Dependencies/IaC | Trivy | Separate PR workflow | HIGH/CRITICAL gate |
| Performance | k6 | Not wired | Staging only, bounded VU/duration/SLO and approved window |

## Stop conditions

Cancel the run and notify the asset owner if latency/error rates rise, unexpected state changes occur, any out-of-scope redirect is found, authorization is revoked, or sensitive data is captured. Preserve only minimal redacted evidence.
