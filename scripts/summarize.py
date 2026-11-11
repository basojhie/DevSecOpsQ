#!/usr/bin/env python3
"""Build a small sanitized run summary; never prints raw scanner evidence."""
import json
from pathlib import Path
out = Path("reports/summary.json")
out.parent.mkdir(exist_ok=True)
summary = {
    "project": "DevSecOpsQ",
    "schema_version": 1,
    "profile": __import__("os").environ.get("ASM_PROFILE", "passive"),
    "scope_gate": __import__("os").environ.get("SCOPE_GATE", "unknown"),
    "files": sorted(p.name for p in Path("reports").glob("*") if p.is_file() and p.name != "summary.json"),
    "notice": "Scanner output requires manual triage. Review artifacts privately; do not publish secrets or raw session data."
}
out.write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
