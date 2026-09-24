# Manual Verification — IC Engine Performance

## Given data

- Dynamometer torque, T = 100 N·m
- Engine speed, N = 1500 RPM
- Fuel mass-flow rate = 5 kg/h
- Petrol calorific value, CV = 44,000 kJ/kg
- Friction power, FP = 2 kW

## 1. Brake power

BP = (2 × π × N × T) / (60 × 1000)

BP = (2 × π × 1500 × 100) / (60 × 1000)

**BP = 15.708 kW**

## 2. Fuel-energy input

Fuel flow = 5 / 3600 = 0.0013889 kg/s

Fuel power = fuel flow × CV

Fuel power = 0.0013889 × 44,000

**Fuel power = 61.111 kW**

## 3. Indicated power

IP = BP + FP = 15.708 + 2

**IP = 17.708 kW**

## 4. Brake specific fuel consumption

BSFC = fuel flow in kg/h / BP in kW

BSFC = 5 / 15.708

**BSFC = 0.31831 kg/kWh = 318.31 g/kWh**

## 5. Brake thermal efficiency

Brake thermal efficiency = (BP / fuel power) × 100

Brake thermal efficiency = (15.708 / 61.111) × 100

**Brake thermal efficiency = 25.704%**

## 6. Mechanical efficiency

Mechanical efficiency = (BP / IP) × 100

Mechanical efficiency = (15.708 / 17.708) × 100

**Mechanical efficiency = 88.706%**

The automated regression test uses these values to verify the application.
