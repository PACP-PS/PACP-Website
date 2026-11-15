#!/usr/bin/env python3
"""Fail-closed checks for manual Cloudflare preview workflow (no deployment)."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Preview(unittest.TestCase):
 def test_preview_requires_explicit_approval(self):
  s=(ROOT/'.github/workflows/manual-pages-preview.yml').read_text()
  self.assertIn('workflow_dispatch:',s)
  self.assertIn("inputs.approval == 'PACP-PREVIEW-APPROVED'",s)
  self.assertIn("refs/heads/rebuild/platform-foundation",s)
  self.assertIn("environment: pacp-preview",s)
  self.assertIn("--branch=rebuild-platform-foundation",s)
  self.assertIn("pages deploy build/pacp-public-preview",s)
  self.assertNotIn("--branch=main",s)
  self.assertNotIn("www.pacp.ps",s)
 def test_archive_job_no_deployment(self):
  s=(ROOT/'.github/workflows/package-original-preview.yml').read_text()
  self.assertIn("python3 scripts/build_public_preview.py",s)
  self.assertIn("build/pacp-public-preview",s)
  self.assertNotIn("pages deploy",s)
  self.assertIn("upload-artifact",s)
if __name__=='__main__':unittest.main(verbosity=2)
