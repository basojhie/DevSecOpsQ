# DevSecOpsQ — Authorized Attack Surface Management

DevSecOpsQ is a scope-gated, low-impact ASM and defensive security assessment pipeline for assets you own or are explicitly authorized to test.

## Safety model

- Every target must be listed in `config/scope.txt` and pass the validator.
- Default profile is `passive`. Active checks are opt-in and restricted to explicitly approved staging targets.
- The workflow never accepts arbitrary target input from an untrusted dispatch payload.
- No exploit, brute-force, credential testing, destructive checks, or production load testing is included.
- Production is limited to passive discovery and low-impact HTTP/TLS metadata checks. Active DAST/path discovery/performance testing require staging approval.
- Keep credentials in GitHub Actions Secrets. Never commit tokens, cookies, or account data.
- Cancel the workflow immediately if the asset owner requests a stop or service health degrades.

## Quick start

1. Edit `config/scope.txt` with one exact domain per line. Do not add third-party/CDN/shared-hosting assets unless their owner explicitly authorized the test.
2. Edit `config/targets.json` to map each domain to `production` or `staging` and record approval metadata.
3. Review `.github/workflows/asm.yml`, tool pins, rate limits and exclusions.
4. Run **Actions → DevSecOpsQ ASM → Run workflow** with the `passive` profile first.
5. Review the generated artifact before enabling optional staging-only checks.

## Pipeline

Scope gate → passive subdomain discovery (Subfinder) → DNS validation (dnsx) → HTTP metadata (httpx) → asset delta (anew) → optional constrained port/service inventory (Naabu/Nmap) → historical URL candidates (gau) → constrained crawl (Katana) → optional staging-only content discovery (ffuf) → TLS review (testssl.sh) → curated Nuclei templates → code/dependency/secret scanning (Semgrep, Gitleaks, Trivy) → JSONL/summary report → optional Telegram notification.

Tool availability varies by runner and upstream release. Pin versions in the workflow and review release notes before upgrades.

## Termux controller

See [docs/TERMUX.md](docs/TERMUX.md). Termux is a remote trigger/status client; scans run on isolated GitHub-hosted runners.

## Configuration

- `config/scope.txt`: exact approved apex domains/hostnames.
- `config/targets.json`: environment and authorization metadata.
- `config/exclude.txt`: explicitly excluded hostnames/IP ranges.
- `config/profiles.json`: documented rate and feature profiles.
- `scripts/validate_scope.py`: fail-closed scope validation.
- `scripts/summarize.py`: sanitized artifact summary.

## Outputs

Workflow artifacts contain discovery inventories and scanner reports. They may still reveal internal asset information; restrict repository and artifact access and set a short retention period.

## Disclaimer

Use only against systems you own or have written permission to assess. Automated findings require manual validation; absence of findings is not proof of security.
