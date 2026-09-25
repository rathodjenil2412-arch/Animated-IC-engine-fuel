# EngineLab — IC Engine Performance Calculator

Python and Streamlit mini project for **Problem No. 10: IC Engine Fuel Consumption & Brake Thermal Efficiency Tool**.

## Student

- **Name:** RATHOD JENIL KUMAR RAVI KUMAR
- **Enrollment No.:** 25012251210003
- **Submission type:** Individual mini project

## What the app does

The app accepts dynamometer torque, engine RPM, fuel mass-flow rate, fuel calorific value, and optional friction power. It calculates:

- Brake power (BP)
- Fuel-energy input
- Indicated power (IP), when friction power is entered
- Brake and indicated specific fuel consumption
- Brake and indicated thermal efficiency
- Mechanical efficiency
- Heat and other energy losses

It also includes a moving piston/crankshaft illustration, fuel-specific ignition hardware, animated efficiency gauge, energy-balance donut chart, performance graph, formula substitution, input validation, a CSV download, and viva notes.

## Technically correct engine animation

- **Petrol mode:** air–fuel mixture enters the cylinder and a spark plug initiates combustion.
- **Diesel mode:** only air enters during intake; a fuel injector sprays diesel near the end of compression and the fuel self-ignites. No spark plug is shown or used.
- **CNG mode:** an air–CNG mixture enters the cylinder and a spark plug initiates combustion. The editable CNG calorific-value preset is 47,000 kJ/kg.
- **Custom fuel mode:** the user can choose either spark ignition or compression ignition.

The animation automatically changes the intake label, ignition hardware, ignition event and four-stroke descriptions when the fuel or ignition system changes.

## Engineering formulas

```text
BP (kW) = 2 × π × RPM × Torque / (60 × 1000)
Fuel power (kW) = (fuel flow in kg/h / 3600) × CV in kJ/kg
IP = BP + friction power
BSFC (kg/kWh) = fuel flow in kg/h / BP in kW
Brake thermal efficiency (%) = BP / fuel power × 100
Mechanical efficiency (%) = BP / IP × 100
```

## Verified example

| Input | Value |
|---|---:|
| Torque | 100 N·m |
| Engine speed | 1500 RPM |
| Petrol fuel flow | 5 kg/h |
| Calorific value | 44,000 kJ/kg |
| Friction power | 2 kW |

Expected key results: **BP = 15.708 kW**, **BSFC = 318.31 g/kWh**, **brake thermal efficiency = 25.704%**, and **mechanical efficiency = 88.706%**.

See `MANUAL_TEST_CASE.md` for the complete hand calculation.

## Project files

```text
app.py                             Streamlit web application
engine_calculations.py             Independent calculation module
requirements.txt                   Deployment dependencies
MANUAL_TEST_CASE.md                Manual verification
tests/test_engine_calculations.py  Regression tests
tests/test_streamlit_app.py         Streamlit smoke test
tests/test_engine_animation.py      Fuel-specific animation tests
.streamlit/config.toml             App theme
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Run calculation tests:

```bash
python -m unittest discover -s tests -v
```

## Deploy on Streamlit Community Cloud

1. Upload all project files to a public GitHub repository.
2. Sign in at `https://share.streamlit.io` using GitHub.
3. Select **Create app** and **Deploy a public app from GitHub**.
4. Select the repository and branch `main`.
5. Set the main file path to `app.py`.
6. Select **Deploy**.
