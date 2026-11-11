# Operations and safe test matrix

| Area | Default automation | Active test constraint |
|---|---|---|
| Asset inventory | Subfinder passive sources, dnsx, anew | Exact allowlist only |
| HTTP metadata | httpx | Low request rate; no redirect outside scope |
| URL history | gau | Historical URLs are candidates, not proof of live routes |
| Crawling | Katana | Disabled by default; staging approval |
| Ports/services | Naabu + Nmap | Explicit staging approval; small selected port set |
| Content discovery | ffuf | Disabled by default; staging approval |
| Vulnerability templates | Nuclei | Curated safe templates only; staging approval |
| TLS | testssl.sh | Low-impact profile; allowlisted endpoints |
| Code/dependencies/secrets | Semgrep, Trivy, Gitleaks | Repository-only; redact secret values |
| DAST | ZAP baseline | Not wired to active scan; use separately reviewed staging config |
| Parameter testing | Dalfox | Not wired to automatic run; manually approved staging test |
| Performance | k6 | Not wired to automatic run; separate staging change window |

## Stop conditions

Cancel the run and notify the asset owner if latency/error rates rise, unexpected state changes occur, any out-of-scope redirect is found, authorization is revoked, or sensitive data is captured. Preserve only minimal redacted evidence.
