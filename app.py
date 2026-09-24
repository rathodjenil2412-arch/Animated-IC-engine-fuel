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
    # A true four-stroke cycle completes in two crankshaft revolutions. The
    # visual rate follows RPM, but is slowed enough for a student to observe
    # valve timing and each stroke clearly.
    duration = max(1.8, min(5.2, 4500.0 / rpm))
    html = f"""
    <!doctype html>
    <html lang="en">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin:0; background:transparent; font-family:Inter,Arial,sans-serif; color:#eef7fa; }}
        .machine {{
            position:relative; height:374px; overflow:hidden;
            background:radial-gradient(circle at 35% 18%,#163d4c 0,#0c222e 38%,#07141d 100%);
            border:1px solid #315366; border-radius:10px;
            box-shadow:inset 0 0 42px rgba(0,0,0,.3);
        }}
        .grid {{
            position:absolute; inset:0; opacity:.12;
            background-image:linear-gradient(#6e8b9a 1px,transparent 1px),linear-gradient(90deg,#6e8b9a 1px,transparent 1px);
            background-size:22px 22px;
        }}
        .topbar {{
            position:absolute; z-index:5; left:0; right:0; top:0; height:46px;
            display:flex; align-items:center; justify-content:space-between;
            padding:0 15px; background:rgba(4,15,22,.72); border-bottom:1px solid #294958;
        }}
        .tag {{ color:#f4f8f9; font-size:12px; font-weight:760; letter-spacing:.1em; }}
        .tag .led {{ display:inline-block; width:7px; height:7px; border-radius:50%; margin-right:7px; background:#46d39a; box-shadow:0 0 10px #46d39a; animation:pulse 1.1s infinite; }}
        .readout {{ display:flex; align-items:center; gap:10px; }}
        .rpm {{ color:#ffad73; font:750 12px ui-monospace,monospace; }}
        .pause {{
            border:1px solid #527183; background:#102b39; color:#dce9ed; border-radius:15px;
            padding:4px 10px; font-size:10px; font-weight:700; cursor:pointer;
        }}
        .pause:hover {{ background:#1a4051; }}
        svg {{ position:absolute; left:0; right:0; top:42px; width:100%; height:276px; }}
        .metal {{ fill:url(#metal); stroke:#9db0ba; stroke-width:2; }}
        .dark-metal {{ fill:#10232e; stroke:#718995; stroke-width:3; }}
        .label {{ fill:#95aab4; font-size:10px; font-weight:700; letter-spacing:.08em; }}
        .small {{ fill:#b9c8ce; font-size:9px; }}
        .data-title {{ fill:#78919d; font-size:9px; font-weight:700; letter-spacing:.1em; }}
        .data-value {{ fill:#f0f6f8; font-size:15px; font-weight:760; }}
        .port {{ fill:none; stroke:#5d7784; stroke-width:23; stroke-linecap:round; }}
        .port-inner {{ fill:none; stroke:#142d39; stroke-width:15; stroke-linecap:round; }}
        .intake-dot {{ fill:#49d3e2; animation:intake-flow 1.05s linear infinite; }}
        .exhaust-dot {{ fill:#ff9a55; animation:exhaust-flow 1.05s linear infinite; }}
        .d2 {{ animation-delay:-.35s; }} .d3 {{ animation-delay:-.7s; }}
        #intakeCloud,#exhaustCloud,#spark,#flame {{ transition:opacity .1s linear; }}
        #flame {{ filter:url(#glow); transform-origin:405px 124px; animation:flame-pulse .16s ease-in-out infinite alternate; }}
        .spark-ray {{ stroke:#fff09c; stroke-width:2.4; stroke-linecap:round; }}
        .valve-head {{ fill:#c8d3d8; stroke:#607985; stroke-width:2; }}
        .phase-strip {{
            position:absolute; z-index:5; left:12px; right:12px; bottom:12px;
            display:grid; grid-template-columns:repeat(4,1fr); gap:7px;
        }}
        .phase {{
            min-width:0; background:rgba(8,26,36,.9); border:1px solid #31505f; border-radius:5px;
            padding:7px 8px; color:#8097a2; transition:.18s ease;
        }}
        .phase b {{ display:block; color:#b8c7cd; font-size:10px; letter-spacing:.06em; }}
        .phase span {{ display:block; font-size:9px; margin-top:2px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }}
        .phase.active {{ background:#143c4b; border-color:#59c4c9; box-shadow:0 0 15px rgba(73,211,226,.18); transform:translateY(-2px); }}
        .phase.active b {{ color:#fff; }}
        .phase.power.active {{ background:#49281b; border-color:#ff8c42; box-shadow:0 0 16px rgba(255,123,42,.22); }}
        @keyframes intake-flow {{ from {{ transform:translateX(-8px); opacity:0; }} 25% {{ opacity:1; }} to {{ transform:translateX(104px); opacity:0; }} }}
        @keyframes exhaust-flow {{ from {{ transform:translateX(0); opacity:0; }} 25% {{ opacity:1; }} to {{ transform:translateX(112px); opacity:0; }} }}
        @keyframes flame-pulse {{ from {{ transform:scale(.88); }} to {{ transform:scale(1.08); }} }}
        @keyframes pulse {{ 50% {{ opacity:.35; box-shadow:0 0 3px #46d39a; }} }}
        @media (max-width:560px) {{
            .machine {{ height:355px; }} .tag {{ font-size:9px; }} .rpm {{ font-size:10px; }}
            .pause {{ padding:3px 7px; }} svg {{ height:263px; }}
            .phase {{ padding:6px 4px; }} .phase b {{ font-size:8px; }} .phase span {{ display:none; }}
        }}
    </style>
    </head>
    <body>
      <div class="machine">
        <div class="grid"></div>
        <div class="topbar">
          <div class="tag"><span class="led"></span>LIVE 4-STROKE DIGITAL TWIN · {fuel_name.upper()}</div>
          <div class="readout"><span class="rpm">{rpm:,.0f} RPM</span><button id="pauseButton" class="pause" type="button">PAUSE</button></div>
        </div>
        <svg viewBox="0 0 840 330" role="img" aria-label="Interactive four-stroke single-cylinder engine animation">
          <defs>
            <linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#edf2f4"/><stop offset=".45" stop-color="#97aab4"/><stop offset="1" stop-color="#dce5e8"/></linearGradient>
            <linearGradient id="pistonMetal" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#f0f4f5"/><stop offset=".52" stop-color="#aab9c0"/><stop offset="1" stop-color="#718792"/></linearGradient>
            <radialGradient id="fire" cx="50%" cy="15%"><stop offset="0" stop-color="#fff7a1"/><stop offset=".38" stop-color="#ffb22d"/><stop offset="1" stop-color="#ef5423" stop-opacity=".15"/></radialGradient>
            <filter id="glow" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
            <clipPath id="boreClip"><rect x="315" y="88" width="180" height="189" rx="4"/></clipPath>
          </defs>

          <!-- Intake and exhaust manifolds -->
          <path d="M55 113 H250 Q285 113 326 139" class="port"/>
          <path d="M55 113 H250 Q285 113 326 139" class="port-inner"/>
          <path d="M483 139 Q525 113 565 113 H650" class="port"/>
          <path d="M483 139 Q525 113 565 113 H650" class="port-inner"/>
          <text x="58" y="88" class="label">AIR + {fuel_name.upper()}</text>
          <text x="548" y="88" class="label">EXHAUST GAS</text>
          <g id="intakeCloud" opacity="0">
            <circle cx="77" cy="113" r="4" class="intake-dot"/><circle cx="104" cy="113" r="4" class="intake-dot d2"/><circle cx="132" cy="113" r="4" class="intake-dot d3"/>
          </g>
          <g id="exhaustCloud" opacity="0">
            <circle cx="518" cy="113" r="4" class="exhaust-dot"/><circle cx="546" cy="113" r="4" class="exhaust-dot d2"/><circle cx="574" cy="113" r="4" class="exhaust-dot d3"/>
          </g>

          <!-- Cylinder head and liner -->
          <path d="M292 82 Q292 62 312 62 H498 Q518 62 518 82 V284 H292 Z" class="dark-metal"/>
          <rect x="310" y="83" width="190" height="199" rx="5" fill="#07151d" stroke="#6e8793" stroke-width="3"/>
          <rect id="chamberFill" x="316" y="89" width="178" height="64" rx="3" fill="#3bb9d0" opacity=".24" clip-path="url(#boreClip)"/>
          <text x="303" y="51" class="label">CYLINDER HEAD</text>

          <!-- Intake valve -->
          <g id="intakeValve">
            <rect x="345" y="49" width="9" height="63" rx="3" class="metal"/>
            <path d="M335 108 H364 L358 118 H341 Z" class="valve-head"/>
          </g>
          <!-- Exhaust valve -->
          <g id="exhaustValve">
            <rect x="457" y="49" width="9" height="63" rx="3" class="metal"/>
            <path d="M447 108 H476 L470 118 H453 Z" class="valve-head"/>
          </g>
          <text x="329" y="39" class="small">INTAKE</text><text x="448" y="39" class="small">EXHAUST</text>

          <!-- Spark plug and combustion -->
          <path d="M397 47 H414 L411 91 H400 Z" fill="#e7ecee" stroke="#7f939c" stroke-width="2"/>
          <path d="M400 55 H411 M399 63 H412 M399 71 H411" stroke="#647985" stroke-width="2"/>
          <g id="spark" opacity="0">
            <line x1="405" y1="91" x2="396" y2="105" class="spark-ray"/><line x1="406" y1="92" x2="415" y2="106" class="spark-ray"/><line x1="405" y1="91" x2="405" y2="109" class="spark-ray"/>
          </g>
          <g id="flame" opacity="0"><path d="M405 94 C430 111 441 137 426 163 C421 144 411 137 405 122 C397 143 387 151 389 170 C363 149 367 116 405 94 Z" fill="url(#fire)"/></g>

          <!-- Piston, connecting rod and crank mechanism -->
          <g id="piston">
            <rect x="323" y="0" width="164" height="45" rx="5" fill="url(#pistonMetal)" stroke="#647b86" stroke-width="3"/>
            <path d="M329 11 H481 M329 19 H481" stroke="#697e88" stroke-width="2"/>
            <circle cx="405" cy="24" r="9" fill="#536c78" stroke="#d6e0e4" stroke-width="3"/>
          </g>
          <line id="rod" x1="405" y1="180" x2="405" y2="298" stroke="#cbd6da" stroke-width="13" stroke-linecap="round"/>
          <circle id="rodTop" cx="405" cy="180" r="8" fill="#e66b24"/>
          <circle cx="405" cy="299" r="50" fill="#0b1b24" stroke="#9eafb7" stroke-width="9"/>
          <circle cx="405" cy="299" r="38" fill="none" stroke="#284653" stroke-width="3" stroke-dasharray="5 6"/>
          <line id="crankArm" x1="405" y1="299" x2="405" y2="257" stroke="#e66b24" stroke-width="10" stroke-linecap="round"/>
          <circle id="crankPin" cx="405" cy="257" r="9" fill="#ffc197" stroke="#8c3a0e" stroke-width="2"/>
          <circle cx="405" cy="299" r="11" fill="#e66b24" stroke="#ffc197" stroke-width="3"/>
          <text x="468" y="310" class="small">CRANKSHAFT</text>

          <!-- Live telemetry -->
          <rect x="672" y="63" width="150" height="62" rx="6" fill="#0b202b" stroke="#315464"/>
          <text x="686" y="82" class="data-title">ACTIVE STROKE</text><text id="strokeValue" x="686" y="109" class="data-value">INTAKE</text>
          <rect x="672" y="137" width="150" height="62" rx="6" fill="#0b202b" stroke="#315464"/>
          <text x="686" y="156" class="data-title">CRANK ANGLE</text><text id="angleValue" x="686" y="183" class="data-value">0° / 720°</text>
          <rect x="672" y="211" width="150" height="62" rx="6" fill="#0b202b" stroke="#315464"/>
          <text x="686" y="230" class="data-title">VALVE STATE</text><text id="valveValue" x="686" y="257" class="data-value">IN OPEN</text>
          <text id="motionValue" x="672" y="294" class="label">PISTON ↓ DOWN</text>
        </svg>

        <div class="phase-strip">
          <div class="phase" data-phase="0"><b>1 · INTAKE</b><span>Air–fuel enters</span></div>
          <div class="phase" data-phase="1"><b>2 · COMPRESSION</b><span>Both valves closed</span></div>
          <div class="phase power" data-phase="2"><b>3 · POWER</b><span>Spark + expansion</span></div>
          <div class="phase" data-phase="3"><b>4 · EXHAUST</b><span>Burnt gas leaves</span></div>
        </div>
      </div>
      <script>
      (() => {{
        const cycleSeconds = {duration:.4f};
        const piston = document.getElementById('piston');
        const rod = document.getElementById('rod');
        const rodTop = document.getElementById('rodTop');
        const crankArm = document.getElementById('crankArm');
        const crankPin = document.getElementById('crankPin');
        const chamber = document.getElementById('chamberFill');
        const intakeValve = document.getElementById('intakeValve');
        const exhaustValve = document.getElementById('exhaustValve');
        const intakeCloud = document.getElementById('intakeCloud');
        const exhaustCloud = document.getElementById('exhaustCloud');
        const spark = document.getElementById('spark');
        const flame = document.getElementById('flame');
        const strokeValue = document.getElementById('strokeValue');
        const angleValue = document.getElementById('angleValue');
        const valveValue = document.getElementById('valveValue');
        const motionValue = document.getElementById('motionValue');
        const phases = [...document.querySelectorAll('.phase')];
        const pauseButton = document.getElementById('pauseButton');
        const names = ['INTAKE', 'COMPRESSION', 'POWER', 'EXHAUST'];
        const valveStates = ['IN OPEN', 'BOTH CLOSED', 'BOTH CLOSED', 'EX OPEN'];
        const gasColors = ['#49d3e2', '#3aa7bd', '#ff7b2f', '#a9785b'];
        const crankX = 405, crankY = 299, radius = 42, rodLength = 120;
        let start = performance.now();
        let pausedAt = 0;
        let paused = false;

        pauseButton.addEventListener('click', () => {{
          if (paused) {{
            start = performance.now() - pausedAt;
            paused = false;
            pauseButton.textContent = 'PAUSE';
          }} else {{
            pausedAt = performance.now() - start;
            paused = true;
            pauseButton.textContent = 'RESUME';
          }}
        }});

        function render(now) {{
          const elapsed = paused ? pausedAt : now - start;
          const progress = (elapsed / (cycleSeconds * 1000)) % 1;
          const cycleDeg = progress * 720;
          const theta = cycleDeg * Math.PI / 180;
          const sinT = Math.sin(theta), cosT = Math.cos(theta);
          const pinX = crankX + radius * sinT;
          const pinY = crankY - radius * cosT;
          const sliderY = crankY - (radius * cosT + Math.sqrt(rodLength * rodLength - radius * radius * sinT * sinT));
          const pistonTop = sliderY - 24;
          const phase = Math.min(3, Math.floor(progress * 4));
          const phasePosition = (progress * 4) % 1;
          const intakeLift = phase === 0 ? Math.sin(phasePosition * Math.PI) * 13 : 0;
          const exhaustLift = phase === 3 ? Math.sin(phasePosition * Math.PI) * 13 : 0;
          const combustion = phase === 2 ? Math.pow(Math.max(0, Math.sin((1 - phasePosition) * Math.PI / 2)), .5) : 0;
          const sparkOn = cycleDeg >= 345 && cycleDeg <= 382;

          piston.setAttribute('transform', `translate(0 ${{pistonTop.toFixed(2)}})`);
          rod.setAttribute('x1', '405'); rod.setAttribute('y1', sliderY.toFixed(2));
          rod.setAttribute('x2', pinX.toFixed(2)); rod.setAttribute('y2', pinY.toFixed(2));
          rodTop.setAttribute('cy', sliderY.toFixed(2));
          crankArm.setAttribute('x2', pinX.toFixed(2)); crankArm.setAttribute('y2', pinY.toFixed(2));
          crankPin.setAttribute('cx', pinX.toFixed(2)); crankPin.setAttribute('cy', pinY.toFixed(2));

          const chamberHeight = Math.max(12, pistonTop - 89);
          chamber.setAttribute('height', chamberHeight.toFixed(2));
          chamber.setAttribute('fill', gasColors[phase]);
          chamber.setAttribute('opacity', phase === 2 ? (0.28 + combustion * .34).toFixed(2) : '.25');
          intakeValve.setAttribute('transform', `translate(0 ${{intakeLift.toFixed(2)}})`);
          exhaustValve.setAttribute('transform', `translate(0 ${{exhaustLift.toFixed(2)}})`);
          intakeCloud.style.opacity = phase === 0 ? '1' : '0';
          exhaustCloud.style.opacity = phase === 3 ? '1' : '0';
          spark.style.opacity = sparkOn ? '1' : '0';
          flame.style.opacity = combustion.toFixed(2);

          strokeValue.textContent = names[phase];
          strokeValue.setAttribute('fill', phase === 2 ? '#ff9a55' : '#f0f6f8');
          angleValue.textContent = `${{Math.round(cycleDeg)}}° / 720°`;
          valveValue.textContent = valveStates[phase];
          motionValue.textContent = `PISTON ${{phase === 0 || phase === 2 ? '↓ DOWN' : '↑ UP'}}`;
          phases.forEach((element, index) => element.classList.toggle('active', index === phase));

          requestAnimationFrame(render);
        }}
        requestAnimationFrame(render);
      }})();
      </script>
    </body>
    </html>
    """
    st.iframe(html, height=382)


def render_efficiency_gauge(efficiency: float) -> None:
    bounded = min(max(efficiency, 0.0), 100.0)
    angle = -90.0 + 1.8 * bounded
    color = "#237a57" if 15.0 <= bounded <= 45.0 else "#e66b24"
    html = f"""
    <!doctype html>
    <html><head><style>
      body {{ margin:0; background:transparent; font-family:Arial,sans-serif; color:#142433; }}
      .box {{ height:374px; background:#fff; border:1px solid #d9dfe2; border-radius:8px; position:relative; overflow:hidden; }}
      .title {{ position:absolute; left:20px; top:17px; color:#62717c; font-size:12px; font-weight:700; letter-spacing:.08em; }}
      .gauge {{ position:absolute; width:210px; height:105px; left:50%; top:100px; transform:translateX(-50%); overflow:hidden; }}
      .arc {{ width:210px; height:210px; border-radius:50%; background:conic-gradient(from 270deg, #dbe2e5 0 50%, transparent 50%); }}
      .arc::after {{ content:""; position:absolute; width:150px; height:150px; border-radius:50%; background:#fff; left:30px; top:30px; }}
      .needle {{ position:absolute; z-index:3; width:85px; height:4px; background:{color}; left:20px; bottom:0; transform-origin:85px 2px; animation:sweep 1.15s cubic-bezier(.2,.7,.2,1) forwards; border-radius:5px; }}
      .hub {{ position:absolute; z-index:4; width:18px; height:18px; background:#142433; border:5px solid {color}; border-radius:50%; left:96px; bottom:-9px; }}
      .value {{ position:absolute; top:224px; left:0; right:0; text-align:center; font-size:31px; font-weight:750; }}
      .caption {{ position:absolute; top:267px; left:18px; right:18px; text-align:center; color:#62717c; font-size:12px; line-height:1.5; }}
      .low,.high {{ position:absolute; top:201px; color:#7b8991; font-size:10px; }}
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
    st.iframe(html, height=382)


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
