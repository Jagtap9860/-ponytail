"""Tests for the adversarial review council."""
import subprocess
import sys

from physics_agent.council.debate import run_council
from physics_agent.council.findings import Finding, median_severity


def test_severity_median():
    assert median_severity(["critical", "high", "critical"]) == "critical"
    assert median_severity(["medium", "low", "low"]) == "low"
    assert median_severity(["high", "low", "medium"]) == "medium"


def _mk(fid, persona, sev, recheck, user_facing=False):
    return Finding(fid, persona, sev, f"t-{fid}", "loc", "ev", recheck, user_facing)


def test_debate_confirms_reproducible():
    v = run_council(checks=[("vex", lambda: [_mk("VEX-T1", "vex", "high", lambda: True)])])
    assert v.findings[0].status == "confirmed"
    assert len(v.findings[0].challenges) == 2  # two rivals cross-examined
    assert v.scoreboard["vex"] > 0


def test_debate_refutes_ghost():
    v = run_council(checks=[("nia", lambda: [_mk("NIA-T1", "nia", "critical", lambda: False)])])
    f = v.findings[0]
    assert f.status == "refuted"
    assert v.scoreboard["nia"] == -2
    # the refuting rival earned +3
    assert any(pts == 3 for p, pts in v.scoreboard.items() if p != "nia")


def test_hardcode_scan_catches_planted_literal(tmp_path):
    from physics_agent.council.checks import _literal_hits
    f = tmp_path / "x.py"
    f.write_text("G0 = 9.80665\nX = 1.5\n")
    assert _literal_hits(f) == [(1, "9.80665")]


def test_full_council_no_open_criticals():
    v = run_council()
    assert v.open_at("critical") == []
    assert v.confirmed == [f for f in v.findings if f.status == "confirmed"]


def test_council_cli_pass():
    r = subprocess.run([sys.executable, "-m", "physics_agent.cli",
                        "council", "review", "--fail-on", "critical"],
                       capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stdout[-2000:] + r.stderr[-1000:]
    assert "council: PASS" in r.stdout
