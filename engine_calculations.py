"""Engineering calculations for the IC Engine Performance Lab app."""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, pi


@dataclass(frozen=True)
class EngineInputs:
    """User inputs expressed in the units displayed by the Streamlit app."""

    torque_nm: float
    rpm: float
    fuel_flow_kg_per_hr: float
    calorific_value_kj_per_kg: float
    friction_power_kw: float = 0.0


@dataclass(frozen=True)
class EngineResults:
    """Calculated IC-engine performance values."""

    brake_power_kw: float
    fuel_power_kw: float
    indicated_power_kw: float
    brake_sfc_kg_per_kwh: float
    brake_sfc_g_per_kwh: float
    indicated_sfc_kg_per_kwh: float
    brake_thermal_efficiency_percent: float
    indicated_thermal_efficiency_percent: float
    mechanical_efficiency_percent: float
    other_losses_kw: float
    brake_energy_share_percent: float
    friction_energy_share_percent: float
    other_loss_share_percent: float


def _require_positive(name: str, value: float) -> None:
    if not isfinite(value) or value <= 0:
        raise ValueError(f"{name} must be greater than zero.")


def validate_inputs(inputs: EngineInputs) -> None:
    """Raise a clear error when the supplied data is not physically usable."""

    _require_positive("Torque", inputs.torque_nm)
    _require_positive("Engine speed", inputs.rpm)
    _require_positive("Fuel mass-flow rate", inputs.fuel_flow_kg_per_hr)
    _require_positive("Calorific value", inputs.calorific_value_kj_per_kg)

    if not isfinite(inputs.friction_power_kw) or inputs.friction_power_kw < 0:
        raise ValueError("Friction power cannot be negative.")


def calculate_performance(inputs: EngineInputs) -> EngineResults:
    """Calculate power, SFC, efficiency, and a first-law energy balance.

    Formula conventions
    -------------------
    Brake power: BP = 2*pi*N*T/60
    Fuel power:   Q_in = m_dot*CV
    Indicated power: IP = BP + FP
    Brake SFC:    BSFC = m_f/BP
    Brake thermal efficiency: eta_bth = BP/Q_in
    """

    validate_inputs(inputs)

    brake_power_kw = (2.0 * pi * inputs.rpm * inputs.torque_nm) / (60.0 * 1000.0)
    fuel_power_kw = (
        inputs.fuel_flow_kg_per_hr / 3600.0
    ) * inputs.calorific_value_kj_per_kg
    indicated_power_kw = brake_power_kw + inputs.friction_power_kw

    if indicated_power_kw > fuel_power_kw + 1e-9:
        raise ValueError(
            "Brake power plus friction power is greater than the fuel-energy input. "
            "Check torque, RPM, fuel flow, calorific value, and units."
        )

    brake_sfc_kg_per_kwh = inputs.fuel_flow_kg_per_hr / brake_power_kw
    indicated_sfc_kg_per_kwh = inputs.fuel_flow_kg_per_hr / indicated_power_kw
    brake_efficiency = 100.0 * brake_power_kw / fuel_power_kw
    indicated_efficiency = 100.0 * indicated_power_kw / fuel_power_kw
    mechanical_efficiency = 100.0 * brake_power_kw / indicated_power_kw
    other_losses_kw = fuel_power_kw - indicated_power_kw

    return EngineResults(
        brake_power_kw=brake_power_kw,
        fuel_power_kw=fuel_power_kw,
        indicated_power_kw=indicated_power_kw,
        brake_sfc_kg_per_kwh=brake_sfc_kg_per_kwh,
        brake_sfc_g_per_kwh=1000.0 * brake_sfc_kg_per_kwh,
        indicated_sfc_kg_per_kwh=indicated_sfc_kg_per_kwh,
        brake_thermal_efficiency_percent=brake_efficiency,
        indicated_thermal_efficiency_percent=indicated_efficiency,
        mechanical_efficiency_percent=mechanical_efficiency,
        other_losses_kw=other_losses_kw,
        brake_energy_share_percent=brake_efficiency,
        friction_energy_share_percent=(
            100.0 * inputs.friction_power_kw / fuel_power_kw
        ),
        other_loss_share_percent=(100.0 * other_losses_kw / fuel_power_kw),
    )


def performance_curve(
    inputs: EngineInputs,
    points: int = 80,
    maximum_torque_factor: float = 1.5,
) -> tuple[list[float], list[float], list[float]]:
    """Return torque, brake-power, and brake-efficiency values for a plot.

    Fuel flow and engine speed remain constant. The upper torque limit is kept
    below the available fuel power so the plotted efficiency stays physical.
    """

    validate_inputs(inputs)
    if points < 2:
        raise ValueError("At least two curve points are required.")

    fuel_power_kw = (
        inputs.fuel_flow_kg_per_hr / 3600.0
    ) * inputs.calorific_value_kj_per_kg
    usable_power_kw = max(fuel_power_kw - inputs.friction_power_kw, 0.0)
    physical_torque_limit = (
        usable_power_kw * 1000.0 * 60.0 / (2.0 * pi * inputs.rpm)
    )
    maximum_torque = max(
        inputs.torque_nm,
        min(
            inputs.torque_nm * maximum_torque_factor,
            physical_torque_limit * 0.98,
        ),
    )
    minimum_torque = max(
        1e-6,
        min(inputs.torque_nm * 0.2, maximum_torque * 0.5),
    )

    step = (maximum_torque - minimum_torque) / (points - 1)
    torques = [minimum_torque + index * step for index in range(points)]
    powers = [
        (2.0 * pi * inputs.rpm * torque) / (60.0 * 1000.0)
        for torque in torques
    ]
    efficiencies = [100.0 * power / fuel_power_kw for power in powers]
    return torques, powers, efficiencies
