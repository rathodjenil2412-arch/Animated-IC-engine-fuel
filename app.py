"""EngineLab: IC-engine fuel consumption and efficiency calculator."""

from __future__ import annotations

from io import StringIO

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from engine_calculations import EngineInputs, calculate_performance, performance_curve


st.set_page_config(
    page_title="EngineLab | IC Engine Performance",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)


STUDENT_NAME = "RATHOD JENIL KUMAR RAVI KUMAR"
ENROLLMENT_NUMBER = "25012251210003"
FUEL_PRESETS = {
    "Petrol": 44_000.0,
    "Diesel": 42_500.0,
    "Custom fuel": 40_000.0,
}


st.markdown(
    """
    <style>
    :root {
        --ink: #142433;
        --muted: #62717c;
        --paper: #f4f1ea;
        --panel: #ffffff;
        --line: #d9dfe2;
        --orange: #e66b24;
        --orange-dark: #b8480a;
        --steel: #25637b;
        --green: #237a57;
    }

    .stApp {
        background:
            linear-gradient(90deg, rgba(20,36,51,.025) 1px, transparent 1px),
            linear-gradient(rgba(20,36,51,.025) 1px, transparent 1px),
            var(--paper);
        background-size: 28px 28px;
        color: var(--ink);
    }

    [data-testid="stSidebar"] {
        background: #152b3a;
        border-right: 1px solid #284657;
    }

    [data-testid="stSidebar"] * { color: #f4f7f8; }
    [data-testid="stSidebar"] label { font-weight: 560; }
    [data-testid="stSidebar"] input { color: #15212c !important; }

    .block-container {
        max-width: 1240px;
        padding-top: 2.1rem;
        padding-bottom: 3rem;
    }

    .hero {
        position: relative;
        overflow: hidden;
        background: #fff;
        border: 1px solid var(--line);
        border-left: 7px solid var(--orange);
        border-radius: 5px;
        box-shadow: 0 12px 34px rgba(31, 48, 60, .08);
        padding: 2.1rem 2.25rem 1.9rem;
        margin-bottom: 1.15rem;
    }

    .hero::after {
        content: "";
        position: absolute;
        width: 185px;
        height: 185px;
        right: -78px;
        top: -95px;
        border: 24px solid rgba(230, 107, 36, .10);
        border-radius: 50%;
    }

    .eyebrow {
        color: var(--orange-dark);
        font-size: .78rem;
        font-weight: 750;
        letter-spacing: .13em;
        text-transform: uppercase;
        margin-bottom: .55rem;
    }

    .hero h1 {
        color: var(--ink);
        font-size: clamp(2.1rem, 5vw, 3.75rem);
        line-height: .98;
        letter-spacing: -.055em;
        margin: 0;
    }

    .hero p {
        color: var(--muted);
        max-width: 790px;
        font-size: 1.02rem;
        line-height: 1.65;
        margin: 1rem 0 0;
    }

    .metric-card {
        min-height: 132px;
        background: var(--panel);
        border: 1px solid var(--line);
        border-top: 4px solid var(--steel);
        border-radius: 5px;
        box-shadow: 0 7px 22px rgba(31, 48, 60, .055);
        padding: 1rem 1.05rem .9rem;
        animation: card-in .55s ease both;
    }

    .metric-card.accent { border-top-color: var(--orange); }
    .metric-label {
        color: var(--muted);
        font-size: .76rem;
        font-weight: 680;
        letter-spacing: .075em;
        text-transform: uppercase;
    }
    .metric-value {
        color: var(--ink);
        font-size: 2rem;
        font-weight: 710;
        line-height: 1.2;
        margin-top: .32rem;
    }
    .metric-unit { color: var(--muted); font-size: .95rem; font-weight: 530; }
    .metric-note { color: #788690; font-size: .72rem; margin-top: .26rem; }

    .section-kicker {
        color: var(--orange-dark);
        font-size: .74rem;
        font-weight: 750;
        letter-spacing: .11em;
        text-transform: uppercase;
        margin-bottom: .2rem;
    }

    .status-strip {
        background: #edf5f0;
        border: 1px solid #c5ddd0;
        border-left: 5px solid var(--green);
        border-radius: 4px;
        color: #184e39;
        padding: .8rem 1rem;
        margin: .5rem 0 1rem;
    }

    .formula-box {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 5px;
        padding: 1rem 1.1rem;
        margin-bottom: .7rem;
    }

    .student-card {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 5px;
        padding: 1rem 1.2rem;
        color: var(--ink);
    }

    .footer-note {
        border-top: 1px solid #ccd4d8;
        color: #66747d;
        font-size: .78rem;
        margin-top: 2.1rem;
        padding-top: 1rem;
        text-align: center;
    }

    div[data-testid="stDownloadButton"] button,
    div[data-testid="stButton"] button {
        border-radius: 4px;
        border: 1px solid var(--orange-dark);
        background: var(--orange);
        color: #fff;
        font-weight: 650;
    }

    @keyframes card-in {
        from { opacity: 0; transform: translateY(8px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @media (max-width: 700px) {
        .block-container { padding: 1rem .8rem 2rem; }
        .hero { padding: 1.45rem 1.15rem 1.3rem; }
        .hero p { font-size: .92rem; }
        .metric-card { min-height: 118px; margin-bottom: .3rem; }
        .metric-value { font-size: 1.72rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def metric_card(
    label: str,
    value: str,
    unit: str,
    note: str,
    accent: bool = False,
) -> None:
    accent_class = " accent" if accent else ""
    st.markdown(
        f"""
        <div class="metric-card{accent_class}">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value} <span class="metric-unit">{unit}</span></div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_engine_animation(rpm: float, fuel_name: str) -> None:
    duration = max(0.65, min(2.0, 2500.0 / rpm))
    html = f"""
    <!doctype html>
    <html>
    <head>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; background: transparent; font-family: Arial, sans-serif; }}
        .machine {{
            position: relative; height: 270px; overflow: hidden;
            background: linear-gradient(145deg, #122532, #1d3a4c);
            border: 1px solid #315366; border-radius: 8px;
        }}
        .grid {{
            position: absolute; inset: 0; opacity: .18;
            background-image: linear-gradient(#6e8b9a 1px, transparent 1px),
                              linear-gradient(90deg, #6e8b9a 1px, transparent 1px);
            background-size: 24px 24px;
        }}
        .tag {{ position:absolute; left:18px; top:15px; color:#f5f7f8; font-size:13px; letter-spacing:.08em; }}
        .rpm {{ position:absolute; right:18px; top:15px; color:#f2a06e; font:700 13px monospace; }}
        svg {{ position:absolute; inset:35px 0 0; width:100%; height:225px; }}
        .piston {{ animation: piston {duration:.3f}s ease-in-out infinite; }}
        .flywheel {{ transform-origin: 330px 152px; animation: spin {duration:.3f}s linear infinite; }}
        .drop1 {{ animation: fuel {duration:.3f}s linear infinite; }}
        .drop2 {{ animation: fuel {duration:.3f}s linear infinite .35s; opacity:0; }}
        @keyframes piston {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(54px); }} }}
        @keyframes spin {{ to {{ transform:rotate(360deg); }} }}
        @keyframes fuel {{ 0% {{ transform:translateY(-15px); opacity:0; }} 25% {{ opacity:1; }} 100% {{ transform:translateY(60px); opacity:0; }} }}
    </style>
    </head>
    <body>
      <div class="machine">
        <div class="grid"></div>
        <div class="tag">LIVE ENGINE CYCLE · {fuel_name.upper()}</div>
        <div class="rpm">{rpm:,.0f} RPM</div>
        <svg viewBox="0 0 430 230" role="img" aria-label="Animated piston and crankshaft">
          <rect x="72" y="25" width="132" height="146" rx="10" fill="#0d1c25" stroke="#6e8795" stroke-width="5"/>
          <rect x="91" y="42" width="94" height="112" rx="5" fill="#172d3b" stroke="#3e5c6c"/>
          <g class="piston">
            <rect x="98" y="50" width="80" height="38" rx="4" fill="#d5dde1" stroke="#879aa4" stroke-width="3"/>
            <line x1="138" y1="88" x2="138" y2="142" stroke="#e66b24" stroke-width="9" stroke-linecap="round"/>
          </g>
          <g class="flywheel">
            <circle cx="330" cy="152" r="58" fill="#10232f" stroke="#d5dde1" stroke-width="9"/>
            <circle cx="330" cy="152" r="12" fill="#e66b24"/>
            <line x1="330" y1="152" x2="330" y2="101" stroke="#e66b24" stroke-width="8" stroke-linecap="round"/>
            <circle cx="330" cy="101" r="8" fill="#f6b188"/>
          </g>
          <path d="M177 155 C220 187, 254 185, 280 160" fill="none" stroke="#8fa3ad" stroke-width="7" stroke-linecap="round"/>
          <path d="M108 18 L108 40" stroke="#f2a06e" stroke-width="4"/>
          <circle class="drop1" cx="108" cy="20" r="5" fill="#f2a06e"/>
          <circle class="drop2" cx="122" cy="17" r="4" fill="#f2a06e"/>
          <text x="72" y="205" fill="#afc0c8" font-size="12">Combustion chamber</text>
          <text x="286" y="225" fill="#afc0c8" font-size="12">Crankshaft output</text>
        </svg>
      </div>
    </body>
    </html>
    """
    st.iframe(html, height=278)


def render_efficiency_gauge(efficiency: float) -> None:
    bounded = min(max(efficiency, 0.0), 100.0)
    angle = -90.0 + 1.8 * bounded
    color = "#237a57" if 15.0 <= bounded <= 45.0 else "#e66b24"
    html = f"""
    <!doctype html>
    <html><head><style>
      body {{ margin:0; background:transparent; font-family:Arial,sans-serif; color:#142433; }}
      .box {{ height:270px; background:#fff; border:1px solid #d9dfe2; border-radius:8px; position:relative; overflow:hidden; }}
      .title {{ position:absolute; left:20px; top:17px; color:#62717c; font-size:12px; font-weight:700; letter-spacing:.08em; }}
      .gauge {{ position:absolute; width:210px; height:105px; left:50%; top:73px; transform:translateX(-50%); overflow:hidden; }}
      .arc {{ width:210px; height:210px; border-radius:50%; background:conic-gradient(from 270deg, #dbe2e5 0 50%, transparent 50%); }}
      .arc::after {{ content:""; position:absolute; width:150px; height:150px; border-radius:50%; background:#fff; left:30px; top:30px; }}
      .needle {{ position:absolute; z-index:3; width:85px; height:4px; background:{color}; left:20px; bottom:0; transform-origin:85px 2px; animation:sweep 1.15s cubic-bezier(.2,.7,.2,1) forwards; border-radius:5px; }}
      .hub {{ position:absolute; z-index:4; width:18px; height:18px; background:#142433; border:5px solid {color}; border-radius:50%; left:96px; bottom:-9px; }}
      .value {{ position:absolute; top:190px; left:0; right:0; text-align:center; font-size:31px; font-weight:750; }}
      .caption {{ position:absolute; top:229px; left:0; right:0; text-align:center; color:#62717c; font-size:12px; }}
      .low,.high {{ position:absolute; top:170px; color:#7b8991; font-size:10px; }}
      .low {{ left:24px; }} .high {{ right:24px; }}
      @keyframes sweep {{ from {{ transform:rotate(-90deg); }} to {{ transform:rotate({angle:.2f}deg); }} }}
    </style></head>
    <body><div class="box">
      <div class="title">BRAKE THERMAL EFFICIENCY</div>
      <div class="gauge"><div class="arc"></div><div class="needle"></div><div class="hub"></div></div>
      <div class="low">0%</div><div class="high">100%</div>
      <div class="value">{bounded:.2f}%</div>
      <div class="caption">Useful brake power ÷ fuel-energy input</div>
    </div></body></html>
    """
    st.iframe(html, height=278)


def make_energy_chart(result, friction_power_kw: float):
    labels = ["Brake output"]
    values = [result.brake_power_kw]
    colors = ["#e66b24"]
    if friction_power_kw > 0:
        labels.append("Friction loss")
        values.append(friction_power_kw)
        colors.append("#78909c")
    labels.append("Heat & other losses")
    values.append(result.other_losses_kw)
    colors.append("#274f65")

    fig, ax = plt.subplots(figsize=(6.2, 4.4))
    fig.patch.set_facecolor("#ffffff")
    wedges, _ = ax.pie(
        values,
        startangle=90,
        counterclock=False,
        colors=colors,
        wedgeprops={"width": 0.35, "edgecolor": "white", "linewidth": 3},
    )
    ax.text(0, 0.09, f"{result.fuel_power_kw:.2f}", ha="center", va="center", fontsize=22, fontweight="bold", color="#142433")
    ax.text(0, -0.12, "kW fuel input", ha="center", va="center", fontsize=10, color="#62717c")
    legend_labels = [f"{label}: {value:.2f} kW" for label, value in zip(labels, values)]
    ax.legend(wedges, legend_labels, loc="lower center", bbox_to_anchor=(0.5, -0.15), ncol=1, frameon=False, fontsize=9)
    ax.set_title("Energy balance", loc="left", fontsize=13, fontweight="bold", color="#142433")
    ax.set_aspect("equal")
    fig.tight_layout()
    return fig


def make_performance_chart(inputs: EngineInputs):
    torques, powers, efficiencies = performance_curve(inputs)
    torques_np = np.asarray(torques)
    powers_np = np.asarray(powers)
    efficiencies_np = np.asarray(efficiencies)

    fig, ax_power = plt.subplots(figsize=(7.2, 4.4))
    fig.patch.set_facecolor("#ffffff")
    ax_power.set_facecolor("#ffffff")
    ax_efficiency = ax_power.twinx()

    power_line = ax_power.plot(
        torques_np, powers_np, color="#e66b24", linewidth=2.6, label="Brake power"
    )[0]
    efficiency_line = ax_efficiency.plot(
        torques_np,
        efficiencies_np,
        color="#25637b",
        linewidth=2.3,
        linestyle="--",
        label="Brake thermal efficiency",
    )[0]
    current = calculate_performance(inputs)
    ax_power.scatter(
        [inputs.torque_nm],
        [current.brake_power_kw],
        s=75,
        color="#142433",
        edgecolor="white",
        linewidth=1.2,
        zorder=5,
        label="Current point",
    )

    ax_power.set_xlabel("Torque (N·m)")
    ax_power.set_ylabel("Brake power (kW)", color="#b8480a")
    ax_efficiency.set_ylabel("Brake thermal efficiency (%)", color="#25637b")
    ax_power.grid(True, color="#d9dfe2", linewidth=0.8, alpha=0.8)
    ax_power.spines[["top", "right"]].set_visible(False)
    ax_efficiency.spines["top"].set_visible(False)
    ax_power.tick_params(colors="#53636e")
    ax_efficiency.tick_params(axis="y", colors="#25637b")
    ax_power.legend(
        handles=[power_line, efficiency_line, ax_power.collections[0]],
        loc="upper left",
        frameon=False,
        fontsize=8.5,
    )
    ax_power.set_title("Constant-speed performance trend", loc="left", fontsize=13, fontweight="bold", color="#142433")
    fig.tight_layout()
    return fig


def make_csv(inputs: EngineInputs, result, fuel_name: str) -> str:
    rows = [
        ("Fuel", fuel_name, "-"),
        ("Torque", inputs.torque_nm, "N m"),
        ("Engine speed", inputs.rpm, "rpm"),
        ("Fuel mass flow", inputs.fuel_flow_kg_per_hr, "kg/h"),
        ("Calorific value", inputs.calorific_value_kj_per_kg, "kJ/kg"),
        ("Friction power", inputs.friction_power_kw, "kW"),
        ("Brake power", result.brake_power_kw, "kW"),
        ("Indicated power", result.indicated_power_kw, "kW"),
        ("Fuel energy input", result.fuel_power_kw, "kW"),
        ("BSFC", result.brake_sfc_kg_per_kwh, "kg/kWh"),
        ("BSFC", result.brake_sfc_g_per_kwh, "g/kWh"),
        ("Brake thermal efficiency", result.brake_thermal_efficiency_percent, "%"),
        ("Indicated thermal efficiency", result.indicated_thermal_efficiency_percent, "%"),
        ("Mechanical efficiency", result.mechanical_efficiency_percent, "%"),
        ("Heat and other losses", result.other_losses_kw, "kW"),
    ]
    output = StringIO()
    output.write("Parameter,Value,Unit\n")
    for parameter, value, unit in rows:
        formatted = f"{value:.6f}" if isinstance(value, float) else str(value)
        output.write(f'"{parameter}","{formatted}","{unit}"\n')
    return output.getvalue()


with st.sidebar:
    st.markdown("## Input panel")
    st.caption("Enter steady-state engine test data using the units shown.")

    st.markdown("### Engine operating data")
    torque_nm = st.number_input(
        "Dynamometer torque (N·m)",
        min_value=0.1,
        max_value=5000.0,
        value=100.0,
        step=5.0,
        help="Measured brake torque at the dynamometer shaft.",
    )
    rpm = st.number_input(
        "Engine speed (RPM)",
        min_value=1.0,
        max_value=20000.0,
        value=1500.0,
        step=50.0,
    )

    st.markdown("### Fuel data")
    fuel_name = st.selectbox("Fuel type", list(FUEL_PRESETS), index=0)
    fuel_flow = st.number_input(
        "Fuel mass-flow rate (kg/h)",
        min_value=0.001,
        max_value=1000.0,
        value=5.0,
        step=0.1,
        format="%.3f",
    )
    calorific_value = st.number_input(
        "Calorific value, CV (kJ/kg)",
        min_value=1000.0,
        max_value=100000.0,
        value=float(FUEL_PRESETS[fuel_name]),
        step=500.0,
        key=f"cv_{fuel_name}",
    )

    st.markdown("### Optional test data")
    include_friction = st.checkbox(
        "Friction power is available",
        value=True,
        help="When selected, indicated power and mechanical efficiency are calculated.",
    )
    friction_power = (
        st.number_input(
            "Friction power (kW)",
            min_value=0.0,
            max_value=1000.0,
            value=2.0,
            step=0.1,
        )
        if include_friction
        else 0.0
    )

    st.markdown("---")
    st.caption("Problem 10 · Diploma in Mechanical Engineering · Semester 3")


inputs = EngineInputs(
    torque_nm=float(torque_nm),
    rpm=float(rpm),
    fuel_flow_kg_per_hr=float(fuel_flow),
    calorific_value_kj_per_kg=float(calorific_value),
    friction_power_kw=float(friction_power),
)

try:
    result = calculate_performance(inputs)
except ValueError as error:
    st.error(str(error), icon="⚠️")
    st.info(
        "Use consistent units: torque in N·m, speed in RPM, fuel flow in kg/h, "
        "calorific value in kJ/kg, and friction power in kW."
    )
    st.stop()


st.markdown(
    """
    <section class="hero">
        <div class="eyebrow">Mechanical Engineering Mini Project · Problem 10</div>
        <h1>EngineLab</h1>
        <p>
            IC-engine fuel consumption and performance calculator for brake power,
            specific fuel consumption, indicated power, thermal efficiency and
            first-law energy balance.
        </p>
    </section>
    """,
    unsafe_allow_html=True,
)


if result.brake_thermal_efficiency_percent < 15:
    status_text = "Low brake thermal efficiency — review operating load and fuel-use data."
elif result.brake_thermal_efficiency_percent <= 45:
    status_text = "Brake thermal efficiency is within a practical IC-engine operating range."
else:
    status_text = "High calculated efficiency — verify the measured fuel flow and calorific value."

st.markdown(f'<div class="status-strip"><strong>Operating assessment:</strong> {status_text}</div>', unsafe_allow_html=True)


tab_performance, tab_calculations, tab_theory = st.tabs(
    ["Performance dashboard", "Formula & verification", "Theory & viva"]
)


with tab_performance:
    visual_column, gauge_column = st.columns([1.45, 1], gap="large")
    with visual_column:
        render_engine_animation(inputs.rpm, fuel_name)
    with gauge_column:
        render_efficiency_gauge(result.brake_thermal_efficiency_percent)

    st.markdown('<div class="section-kicker">Calculated output</div>', unsafe_allow_html=True)
    row_one = st.columns(4, gap="small")
    with row_one[0]:
        metric_card("Brake power", f"{result.brake_power_kw:.2f}", "kW", "Power available at the crankshaft", True)
    with row_one[1]:
        metric_card("Fuel-energy input", f"{result.fuel_power_kw:.2f}", "kW", "Mass flow × calorific value")
    with row_one[2]:
        metric_card("Brake SFC", f"{result.brake_sfc_g_per_kwh:.1f}", "g/kWh", "Fuel required per brake-energy output")
    with row_one[3]:
        metric_card("Brake efficiency", f"{result.brake_thermal_efficiency_percent:.2f}", "%", "Brake power ÷ fuel-energy input", True)

    st.write("")
    row_two = st.columns(3, gap="small")
    with row_two[0]:
        if include_friction:
            metric_card("Indicated power", f"{result.indicated_power_kw:.2f}", "kW", "Brake power + friction power")
        else:
            metric_card("Indicated power", "—", "", "Enter friction power to calculate")
    with row_two[1]:
        if include_friction:
            metric_card("Mechanical efficiency", f"{result.mechanical_efficiency_percent:.2f}", "%", "Brake power ÷ indicated power")
        else:
            metric_card("Mechanical efficiency", "—", "", "Requires friction-power data")
    with row_two[2]:
        metric_card("Heat & other losses", f"{result.other_losses_kw:.2f}", "kW", "Unconverted fuel-energy rate")

    st.write("")
    chart_left, chart_right = st.columns([1, 1.28], gap="large")
    with chart_left:
        energy_figure = make_energy_chart(result, inputs.friction_power_kw)
        st.pyplot(energy_figure, width="stretch")
        plt.close(energy_figure)
    with chart_right:
        performance_figure = make_performance_chart(inputs)
        st.pyplot(performance_figure, width="stretch")
        plt.close(performance_figure)

    st.download_button(
        "Download calculation summary (CSV)",
        data=make_csv(inputs, result, fuel_name),
        file_name="engine_performance_summary.csv",
        mime="text/csv",
        width="stretch",
    )


with tab_calculations:
    st.markdown("### Formula sheet")
    formula_left, formula_right = st.columns(2, gap="large")
    with formula_left:
        st.markdown('<div class="formula-box"><strong>1. Brake power</strong></div>', unsafe_allow_html=True)
        st.latex(r"BP = \frac{2\pi NT}{60\times1000}")
        st.caption("N in RPM, T in N·m, BP in kW")

        st.markdown('<div class="formula-box"><strong>2. Fuel-energy rate</strong></div>', unsafe_allow_html=True)
        st.latex(r"\dot{Q}_{in}=\frac{\dot{m}_f}{3600}\times CV")
        st.caption("Fuel flow in kg/h and CV in kJ/kg give kW")

        st.markdown('<div class="formula-box"><strong>3. Indicated power</strong></div>', unsafe_allow_html=True)
        st.latex(r"IP = BP + FP")
    with formula_right:
        st.markdown('<div class="formula-box"><strong>4. Brake specific fuel consumption</strong></div>', unsafe_allow_html=True)
        st.latex(r"BSFC=\frac{\dot{m}_f}{BP}")

        st.markdown('<div class="formula-box"><strong>5. Brake thermal efficiency</strong></div>', unsafe_allow_html=True)
        st.latex(r"\eta_{bth}=\frac{BP}{\dot{Q}_{in}}\times100")

        st.markdown('<div class="formula-box"><strong>6. Mechanical efficiency</strong></div>', unsafe_allow_html=True)
        st.latex(r"\eta_m=\frac{BP}{IP}\times100")

    st.markdown("### Current calculation — substituted values")
    st.code(
        f"""Brake power
BP = 2 × π × {inputs.rpm:.2f} × {inputs.torque_nm:.2f} / (60 × 1000)
BP = {result.brake_power_kw:.4f} kW

Fuel-energy input
Q_in = ({inputs.fuel_flow_kg_per_hr:.4f} / 3600) × {inputs.calorific_value_kj_per_kg:.2f}
Q_in = {result.fuel_power_kw:.4f} kW

Brake specific fuel consumption
BSFC = {inputs.fuel_flow_kg_per_hr:.4f} / {result.brake_power_kw:.4f}
BSFC = {result.brake_sfc_kg_per_kwh:.5f} kg/kWh = {result.brake_sfc_g_per_kwh:.2f} g/kWh

Brake thermal efficiency
eta_bth = ({result.brake_power_kw:.4f} / {result.fuel_power_kw:.4f}) × 100
eta_bth = {result.brake_thermal_efficiency_percent:.3f}%""",
        language="text",
    )

    st.markdown("### Textbook verification case")
    st.caption("The default inputs are the verified test case supplied with the project.")
    verification_data = {
        "Quantity": ["Brake power", "Fuel input", "BSFC", "Brake thermal efficiency", "Mechanical efficiency"],
        "Manual answer": ["15.708 kW", "61.111 kW", "318.310 g/kWh", "25.704%", "88.706%"],
        "App result": [
            f"{result.brake_power_kw:.3f} kW",
            f"{result.fuel_power_kw:.3f} kW",
            f"{result.brake_sfc_g_per_kwh:.3f} g/kWh",
            f"{result.brake_thermal_efficiency_percent:.3f}%",
            f"{result.mechanical_efficiency_percent:.3f}%" if include_friction else "Friction power not entered",
        ],
    }
    st.table(verification_data)


with tab_theory:
    st.markdown("### Engineering interpretation")
    st.write(
        "A dynamometer measures the torque produced at the engine crankshaft. "
        "Combining torque with rotational speed gives brake power. The chemical "
        "energy supplied by the fuel is found from fuel mass flow and calorific value. "
        "Their ratio gives brake thermal efficiency."
    )

    theory_left, theory_right = st.columns(2, gap="large")
    with theory_left:
        st.markdown("#### What each result means")
        st.markdown(
            """
            - **Brake power (BP):** usable shaft power measured by the dynamometer.
            - **Indicated power (IP):** power developed inside the cylinder.
            - **Friction power (FP):** IP − BP; consumed by mechanical friction and auxiliaries.
            - **BSFC:** fuel required to produce one kWh of brake output; lower is generally better.
            - **Brake thermal efficiency:** percentage of fuel energy converted into brake output.
            """
        )
    with theory_right:
        st.markdown("#### Viva-ready questions")
        with st.expander("Why is indicated power greater than brake power?"):
            st.write("Part of the cylinder power is consumed by friction, pumping, and engine auxiliaries before power reaches the shaft.")
        with st.expander("Why is fuel flow converted from kg/h to kg/s?"):
            st.write("A kW is a kJ per second, so the mass-flow time unit must be seconds when CV is in kJ/kg.")
        with st.expander("What does a lower BSFC indicate?"):
            st.write("The engine uses less fuel to produce the same brake-energy output, so fuel economy is better.")
        with st.expander("Why can thermal efficiency not exceed 100%?"):
            st.write("The shaft output cannot be greater than the chemical energy entering with the fuel; energy is also lost through exhaust, cooling, and friction.")

    st.warning(
        "This educational calculator assumes steady operation and consistent measured data. "
        "It is not a substitute for certified engine-test instrumentation."
    )


st.markdown("### Student details")
st.markdown(
    f"""
    <div class="student-card">
        <strong>{STUDENT_NAME}</strong><br>
        Enrollment No. {ENROLLMENT_NUMBER}<br>
        Individual Mini Project · Problem No. 10
    </div>
    <div class="footer-note">
        Built with Python, Streamlit, NumPy and Matplotlib · IC Engine Performance Lab
    </div>
    """,
    unsafe_allow_html=True,
)
