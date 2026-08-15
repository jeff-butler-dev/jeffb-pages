#!/usr/bin/env python3
"""Fail closed when deployable Pages assets contain private data or credentials."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = ROOT / "site"
# A public static catalog needs no arbitrary uploads. Fail closed on every
# unexpected file type rather than accidentally deploying opaque data.
ALLOWED_EXTENSIONS = {".html", ".htm", ".css", ".js", ".json", ".svg", ".txt"}
DENYLIST = ROOT / "scripts" / "public-denylist.txt"

RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("email address", re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")),
    ("US phone number", re.compile(r"(?<!\d)(?:\+1[ .-]?)?(?:\(?\d{3}\)?[ .-]?)\d{3}[ .-]\d{4}(?!\d)")),
    ("US Social Security number", re.compile(r"(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)")),
    ("Windows home path", re.compile(r"(?i)(?:[A-Z]:\\Users\\|/c/Users/)")),
    ("Unix home path", re.compile(r"(?<![\w/])/(?:home|Users)/[A-Za-z0-9_.-]+")),
    ("private key", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("credential in URL", re.compile(r"(?i)https?://[^\s/@]+:[^\s/@]+@")),
    ("authorization bearer token", re.compile(r"(?i)authorization\s*[:=]\s*bearer\s+[A-Za-z0-9._-]+")),
    ("street-style address", re.compile(r"(?i)\b\d{1,5}\s+[A-Z][A-Za-z.'-]+(?:\s+[A-Z][A-Za-z.'-]+){0,3}\s+(?:street|st\.?|avenue|ave\.?|road|rd\.?|drive|dr\.?|lane|ln\.?|court|ct\.?|boulevard|blvd\.?)\b")),
    ("personal-profile wording", re.compile(r"(?i)\b(?:you own|you have|you stopped|your (?:library|folder|shelf|watchlist|media)|what you said you loved|you've (?:done|cleared|seen|read))\b")),
)


def deployable_files() -> list[Path]:
    if not SITE_ROOT.is_dir():
        raise FileNotFoundError(f"Missing deployable site directory: {SITE_ROOT}")
    files = sorted(p for p in SITE_ROOT.rglob("*") if p.is_file())
    unsupported = [p.relative_to(SITE_ROOT) for p in files if p.suffix.lower() not in ALLOWED_EXTENSIONS]
    if unsupported:
        raise ValueError("Unsupported public asset type(s): " + ", ".join(map(str, unsupported)))
    return files


def main() -> int:
    terms = [line.strip().lower() for line in DENYLIST.read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.lstrip().startswith("#")]
    findings: list[str] = []
    for path in deployable_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), 1):
            for label, rule in RULES:
                if rule.search(line):
                    findings.append(f"{path.relative_to(SITE_ROOT)}:{line_number}: {label}")
            folded = line.lower()
            for term in terms:
                if term in folded:
                    findings.append(f"{path.relative_to(SITE_ROOT)}:{line_number}: blocked personal identifier ({term})")
    if findings:
        print("PUBLICATION BLOCKED: private data or a credential was found:", file=sys.stderr)
        print("\n".join(f"- {item}" for item in findings), file=sys.stderr)
        return 1
    print(f"Public-site safety check passed ({len(deployable_files())} deployable files scanned).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
