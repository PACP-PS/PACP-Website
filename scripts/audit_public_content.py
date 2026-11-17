#!/usr/bin/env python3
"""Non-destructive content QA of the generated public-only PACP preview."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
site = root / "build/pacp-public-preview"
if not site.exists():
    print("ERROR: public preview is missing; run build_public_preview.py first")
    sys.exit(1)

# Some informational pages intentionally discuss staged features; they must clearly disclose status.
placeholder_patterns = {
    "generic course title": r"عنوان (?:ال)?دورة(?: أخرى)?",
    "sample item wording": r"(?:خبر|إعلان|فعالية) (?:تجريبي|تجريبية|نموذجي|نموذجية)",
    "Latin placeholder": r"\b(?:lorem ipsum|coming soon placeholder|example course)\b",
}
issues = []
for page in sorted(site.rglob("*.html")):
    text = page.read_text(encoding="utf-8")
    visible = re.sub(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>", " ", text, flags=re.I|re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    visible = re.sub(r"\s+", " ", visible)
    for label, pattern in placeholder_patterns.items():
        if re.search(pattern, visible, re.I):
            issues.append(f"{page.relative_to(site)}: {label}")
print(f"Public-content audit: {len(list(site.rglob('*.html')))} pages")
for issue in issues:
    print("CONTENT REVIEW NEEDED:", issue)
# Report without unilaterally removing possibly useful public content.
print(f"Content review findings: {len(issues)}")
if issues:
    print("CAUTION: do not promote preview to production before editorial approval.")
