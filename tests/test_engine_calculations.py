"""Regression tests for the solved IC-engine example."""

import unittest

from engine_calculations import (
    EngineInputs,
    calculate_performance,
    performance_curve,
)


class EngineCalculationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.example = EngineInputs(
            torque_nm=100.0,
            rpm=1500.0,
            fuel_flow_kg_per_hr=5.0,
            calorific_value_kj_per_kg=44000.0,
            friction_power_kw=2.0,
        )

    def test_manual_example(self) -> None:
        result = calculate_performance(self.example)
        self.assertAlmostEqual(result.brake_power_kw, 15.70796327, places=7)
        self.assertAlmostEqual(result.fuel_power_kw, 61.11111111, places=7)
        self.assertAlmostEqual(result.indicated_power_kw, 17.70796327, places=7)
        self.assertAlmostEqual(result.brake_sfc_kg_per_kwh, 0.31830989, places=7)
        self.assertAlmostEqual(result.brake_sfc_g_per_kwh, 318.30988618, places=6)
        self.assertAlmostEqual(
            result.brake_thermal_efficiency_percent, 25.70393989, places=6
        )
        self.assertAlmostEqual(
            result.mechanical_efficiency_percent, 88.70564633, places=6
        )
        self.assertAlmostEqual(result.other_losses_kw, 43.40314784, places=6)

    def test_energy_balance_closes(self) -> None:
        result = calculate_performance(self.example)
        output_total = (
            result.brake_power_kw
            + self.example.friction_power_kw
            + result.other_losses_kw
        )
        self.assertAlmostEqual(output_total, result.fuel_power_kw, places=10)
        share_total = (
            result.brake_energy_share_percent
            + result.friction_energy_share_percent
            + result.other_loss_share_percent
        )
        self.assertAlmostEqual(share_total, 100.0, places=10)

    def test_impossible_energy_balance_is_rejected(self) -> None:
        invalid = EngineInputs(
            torque_nm=600.0,
            rpm=3000.0,
            fuel_flow_kg_per_hr=1.0,
            calorific_value_kj_per_kg=42000.0,
            friction_power_kw=5.0,
        )
        with self.assertRaises(ValueError):
            calculate_performance(invalid)

    def test_performance_curve_is_monotonic(self) -> None:
        torques, powers, efficiencies = performance_curve(self.example, points=20)
        self.assertEqual(len(torques), 20)
        self.assertTrue(all(a < b for a, b in zip(torques, torques[1:])))
        self.assertTrue(all(a < b for a, b in zip(powers, powers[1:])))
        self.assertTrue(all(a < b for a, b in zip(efficiencies, efficiencies[1:])))


if __name__ == "__main__":
    unittest.main()
