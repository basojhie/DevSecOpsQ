# DevSecOpsQ — Authorized Attack Surface Management

DevSecOpsQ is a scope-gated, low-impact ASM and defensive security assessment pipeline for assets you own or are explicitly authorized to test.

## Safety model

- Every target must be listed in `config/scope.txt` and have an exact matching record in `config/targets.json`.
- Default profile is `passive`. The target registry must not be empty: an empty registry fails closed.
- Staging assessment requires every target to be tagged staging with `active_testing_approved: true` and an authorization reference.
- Discovered subdomains are filtered back to the approved root domain before any follow-on network tool receives them. Redirects and third-party/CDN assets are not implicitly authorized.
- No exploit, brute-force, credential testing, destructive checks, or production load testing is included.
- Automated active DAST, Nuclei, Dalfox, ffuf and k6 are deliberately not wired as unattended steps; they require separately reviewed test inputs and approval.
- Keep credentials in GitHub Actions Secrets. Never commit tokens, cookies, or account data.

## Quick start

1. Add one exact domain per line to `config/scope.txt`.
2. Add matching target objects to `config/targets.json`, including environment and a written-approval reference.
3. Run **Actions → DevSecOpsQ ASM → Run workflow** with `passive` first.
4. Staging assessments require explicit approval in the registry and should run only in a controlled maintenance window.

## Pipeline

Scope gate → passive subdomain discovery (Subfinder) → exact-root filtering → DNS validation (dnsx) → HTTP metadata (httpx) → asset delta (anew) → historical URL candidates (gau) → optional staging-only constrained port/service inventory (Naabu/Nmap) and crawl (Katana) → sanitized reports.

Repository security is handled separately by GitHub Actions using Semgrep, Gitleaks and Trivy. The operational matrix and Termux controller are documented under `docs/`.

## Limitations and next steps

Cloudflare R2 baseline persistence, Telegram alerts, OWASP ZAP baseline, curated Nuclei templates, TLS assessment, and manual WSTG/API checklist tracking are documented extension points; they are not represented as deployed until credentials, pinned versions, safe templates and integration tests are configured. Review reports privately and manually validate findings.

The initial baseline file is runner-local, so delta history currently resets between clean GitHub-hosted runs. Configure a protected persistent backend (for example Cloudflare R2 with least-privilege credentials and retention policy) before treating cross-run change detection as operational.

Use only against systems you own or have written permission to assess. Automated findings require manual validation; absence of findings is not proof of security.
