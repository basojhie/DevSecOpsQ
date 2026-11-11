#!/usr/bin/env python3
"""Fail-closed authorization and target scope gate for DevSecOpsQ."""
from __future__ import annotations
import ipaddress, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ROOT / "config/scope.txt"
TARGETS = ROOT / "config/targets.json"
EXCLUDES = ROOT / "config/exclude.txt"
DOMAIN_RE = re.compile(r"^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$", re.I)

def lines(path: Path):
    if not path.exists():
        return []
    return [x.strip().lower().rstrip(".") for x in path.read_text().splitlines()
            if x.strip() and not x.lstrip().startswith("#")]

def valid_domain(value: str) -> bool:
    value = value.lower().rstrip(".")
    if "/" in value or ":" in value or "*" in value or "@" in value:
        return False
    try:
        ipaddress.ip_address(value)
        return False
    except ValueError:
        return bool(DOMAIN_RE.fullmatch(value))

def main() -> int:
    try:
        scope = lines(SCOPE)
        excludes = set(lines(EXCLUDES))
        data = json.loads(TARGETS.read_text())
    except Exception as exc:
        print(f"SCOPE_GATE=FAIL config_error={type(exc).__name__}")
        return 2
    if not isinstance(data, dict) or not isinstance(data.get("targets"), list):
        print("SCOPE_GATE=FAIL reason=invalid_target_registry")
        return 2
    entries = data["targets"]
    if not scope or not entries:
        print("SCOPE_GATE=FAIL reason=empty_or_invalid_scope")
        return 2
    if len(scope) != len(set(scope)) or any(not valid_domain(x) for x in scope):
        print("SCOPE_GATE=FAIL reason=invalid_or_duplicate_domain")
        return 2
    approved = {}
    for item in entries:
        if not isinstance(item, dict):
            print("SCOPE_GATE=FAIL reason=invalid_target_record")
            return 2
        domain = str(item.get("domain", "")).lower().rstrip(".")
        if not valid_domain(domain) or domain in approved:
            print("SCOPE_GATE=FAIL reason=invalid_or_duplicate_target")
            return 2
        if item.get("environment") not in ("staging", "production"):
            print("SCOPE_GATE=FAIL reason=environment_required")
            return 2
        if not str(item.get("authorization_ref", "")).strip():
            print("SCOPE_GATE=FAIL reason=authorization_reference_required")
            return 2
        if not isinstance(item.get("active_testing_approved", False), bool):
            print("SCOPE_GATE=FAIL reason=invalid_active_approval")
            return 2
        approved[domain] = item
    if set(scope) != set(approved):
        print("SCOPE_GATE=FAIL reason=scope_targets_mismatch")
        return 2
    for domain in approved:
        if domain in excludes:
            print("SCOPE_GATE=FAIL reason=target_excluded")
            return 2
    profile = sys.argv[1] if len(sys.argv) > 1 else "passive"
    if profile not in ("passive", "staging_assessment"):
        print("SCOPE_GATE=FAIL reason=unknown_profile")
        return 2
    if profile == "staging_assessment":
        bad = [d for d, x in approved.items()
               if x["environment"] != "staging" or x.get("active_testing_approved") is not True]
        if bad:
            print("SCOPE_GATE=FAIL reason=staging_approval_missing")
            return 2
    Path("approved-targets.txt").write_text("\n".join(sorted(approved)) + "\n")
    print(f"SCOPE_GATE=PASS profile={profile} approved_targets={len(approved)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
