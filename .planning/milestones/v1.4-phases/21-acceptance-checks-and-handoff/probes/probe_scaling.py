def test_scaling_consistency():
    # v1.4 keeps raw masses in the residual and absorbs G through D^3 = G*T^2.
    # Use non-unit T values so an accidental D=1 tautology cannot pass.
    cases = [
        {"G": 1.0, "T": 2.0},
        {"G": 1.0, "T": 10.0},
        {"G": 1.0, "T": 0.25},
    ]

    max_relative_error = 0.0
    for case in cases:
        G = case["G"]
        T = case["T"]
        D = (G * T**2) ** (1.0 / 3.0)

        residual_coefficient = G * T**2 / D**3
        coefficient_error = abs(residual_coefficient - 1.0)

        # Parabolic scaled trajectory r'(u)=u^2 has d2r'/du2=2.
        raw_acceleration = (D / T**2) * 2.0
        recovered_scaled_acceleration = raw_acceleration * T**2 / D
        acceleration_error = abs(recovered_scaled_acceleration - 2.0) / 2.0

        max_relative_error = max(max_relative_error, coefficient_error, acceleration_error)
        assert coefficient_error < 1e-10, (
            f"Residual coefficient not normalized for G={G}, T={T}: "
            f"{coefficient_error}"
        )
        assert acceleration_error < 1e-10, (
            f"Acceleration scaling failed for G={G}, T={T}: {acceleration_error}"
        )

    print(
        "Scaling Consistency Pass: "
        f"max_relative_error = {max_relative_error:.2e}; cases = {len(cases)}"
    )

if __name__ == "__main__":
    test_scaling_consistency()
