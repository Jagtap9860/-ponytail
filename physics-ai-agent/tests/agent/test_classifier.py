from physics_agent.agent.classifier import classify


def test_spring_classified_vibrations():
    c = classify("A 10 kg mass is attached to a spring with k = 500 N/m. Find its natural frequency.")
    assert c.domain == "vibrations"
    assert c.needs_numeric


def test_ansys_resonance():
    c = classify("My ANSYS modal analysis shows 217 Hz while excitation is 215 Hz.")
    assert c.domain in ("vibrations", "fea")


def test_bernoulli_fluids():
    assert classify("Use Bernoulli to find pipe velocity from pressure.").domain == "fluid_mechanics"


def test_photon_quantum():
    assert classify("Photon energy of green light wavelength 532 nm.").domain == "quantum_mechanics"


def test_tools_suggested():
    c = classify("Solve the eigenvalue problem for modal frequencies and plot the FRF.")
    assert "solve_eigenvalue_problem" in c.suggested_tools
    assert "plot_function" in c.suggested_tools
