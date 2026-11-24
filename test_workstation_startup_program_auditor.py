import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import audit

def row(workstation, program, publisher, impact, enabled):
    return {"workstation": workstation, "program": program,
            "publisher": publisher, "impact": impact, "enabled": enabled}

class TestStartupAuditor(unittest.TestCase):
    def test_unknown_publisher_is_review(self):
        r = audit([row("WS-01", "SpeedBooster Pro", "UnknownSoft", "high", "yes")])
        self.assertEqual((r[0][3], r[0][4]), ("REVIEW", "unknown publisher, high impact"))

    def test_unknown_publisher_low_impact(self):
        r = audit([row("WS-01", "OldToolbar", "UnknownSoft", "low", "no")])
        self.assertEqual((r[0][3], r[0][4]), ("REVIEW", "unknown publisher"))

    def test_high_impact_known_is_slow_boot(self):
        r = audit([row("WS-03", "HP Support Assistant", "HP", "high", "yes")])
        self.assertEqual((r[0][3], r[0][4]), ("SLOW BOOT", "high startup impact"))

    def test_disabled_known_is_disabled(self):
        r = audit([row("WS-03", "Skype", "Microsoft", "low", "no")])
        self.assertEqual((r[0][3], r[0][4]), ("DISABLED", "not enabled at startup"))

    def test_normal_program_is_ok(self):
        r = audit([row("WS-01", "OneDrive", "Microsoft", "low", "yes")])
        self.assertEqual((r[0][3], r[0][4]), ("OK", ""))

    def test_review_comes_first(self):
        r = audit([row("WS-01", "OneDrive", "Microsoft", "low", "yes"),
                   row("WS-02", "ShadyApp", "UnknownSoft", "low", "yes")])
        self.assertEqual(r[0][1], "ShadyApp")

    def test_empty_input(self):
        self.assertEqual(audit([]), [])
