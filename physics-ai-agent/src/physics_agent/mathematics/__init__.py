"""Mathematical methods: linear algebra, calculus helpers, ODE/PDE utilities."""
from physics_agent.mathematics.numerical_methods import (
    linear_solve,
    least_squares,
    condition_number,
    gradient_descent,
    monte_carlo_pi,
    sensitivity_table,
)
from physics_agent.mathematics.differential_equations import (
    heat_equation_explicit,
    wave_equation_leapfrog,
)

__all__ = [
    "linear_solve", "least_squares", "condition_number", "gradient_descent",
    "monte_carlo_pi", "sensitivity_table", "heat_equation_explicit", "wave_equation_leapfrog",
]
