#!/usr/bin/env python3
"""Verify release cannot pass with incomplete evidence."""
import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestReleaseGate(unittest.TestCase):
    def test_unapproved_release_rejected(self):
        p=subprocess.run([sys.executable,str(ROOT/"scripts/check_release_evidence.py")],cwd=ROOT,capture_output=True,text=True,check=False)
        self.assertNotEqual(p.returncode,0)
        self.assertIn("BLOCKED",p.stdout)
if __name__=="__main__":unittest.main(verbosity=2)
