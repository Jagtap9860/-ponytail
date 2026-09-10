import pytest

from physics_agent.agent.orchestrator import Orchestrator


def test_spring_end_to_end():
    ans = Orchestrator().solve(
        "A 10 kg mass is attached to a spring with k = 500 N/m. Find its natural frequency.")
    assert ans.result["fn_hz"] == pytest.approx(1.1254, rel=1e-3)
    assert "fn =" in ans.report() or "Final Answer" in ans.report()


def test_machine_end_to_end():
    ans = Orchestrator().solve(
        "I have a 20 kg machine mounted on a spring with stiffness 50000 N/m "
        "and damping coefficient 100 Ns/m. What is its natural frequency and resonance behavior?")
    assert ans.result["zeta"] == pytest.approx(0.05, rel=1e-9)
    assert ans.verification.all_passed


def test_resonance_discussion():
    ans = Orchestrator().solve(
        "My ANSYS modal analysis shows a natural frequency of 217 Hz while my "
        "operating excitation is 215 Hz. What does this mean?")
    assert "0.92" in ans.report() and "participation" in ans.report().lower()


def test_newton_end_to_end():
    ans = Orchestrator().solve("F = 100 N, m = 10 kg. Find the acceleration a in m/s^2.")
    assert "10" in ans.report()


def test_conversion_shortcut():
    ans = Orchestrator().solve("convert 3000 rpm to rad/s")
    assert ans.result["value"] == pytest.approx(314.159, rel=1e-4)


def test_missing_data_asks():
    ans = Orchestrator().solve("What is the vibration of my machine?")
    assert "Missing minimum data" in ans.report()


def test_exam_mode_no_answer():
    ans = Orchestrator(mode="exam").solve("A 10 kg mass, k = 500 N/m. Find fn.")
    assert ans.result is None and "Hint" in ans.report()


def test_guided_mode_question():
    ans = Orchestrator(mode="guided").solve("A 10 kg mass, k = 500 N/m. Find fn.")
    assert "your turn" in ans.report()
