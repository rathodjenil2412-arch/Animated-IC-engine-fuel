"""Regression tests for fuel-specific four-stroke animation hardware."""

from __future__ import annotations

import ast
from pathlib import Path
import unittest


APP_FILE = Path(__file__).resolve().parents[1] / "app.py"


class StreamlitStub:
    """Capture the HTML passed to st.iframe without importing Streamlit."""

    def __init__(self) -> None:
        self.html = ""
        self.height = 0

    def iframe(self, html: str, height: int) -> None:
        self.html = html
        self.height = height


def load_animation_function():
    tree = ast.parse(APP_FILE.read_text(encoding="utf-8"))
    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "render_engine_animation"
    )
    module = ast.Module(body=[function], type_ignores=[])
    ast.fix_missing_locations(module)
    stub = StreamlitStub()
    namespace = {"st": stub}
    exec(compile(module, str(APP_FILE), "exec"), namespace)
    return namespace["render_engine_animation"], stub


class EngineAnimationTests(unittest.TestCase):
    def test_diesel_mode_uses_injector_and_no_spark_plug(self) -> None:
        render, stub = load_animation_function()
        render(1500.0, "Diesel", "Compression ignition")

        self.assertIn('aria-label="Fuel injector"', stub.html)
        self.assertIn("FUEL INJECTOR", stub.html)
        self.assertIn("AIR ONLY", stub.html)
        self.assertIn("Injection + self-ignition", stub.html)
        self.assertNotIn('aria-label="Spark plug"', stub.html)
        self.assertNotIn('aria-label="Spark ignition event"', stub.html)

    def test_petrol_mode_uses_spark_plug_and_mixture(self) -> None:
        render, stub = load_animation_function()
        render(1500.0, "Petrol", "Spark ignition")

        self.assertIn('aria-label="Spark plug"', stub.html)
        self.assertIn("SPARK PLUG", stub.html)
        self.assertIn("AIR + PETROL", stub.html)
        self.assertIn("Spark ignition + expansion", stub.html)
        self.assertNotIn('aria-label="Fuel injector"', stub.html)

    def test_cng_mode_uses_spark_plug_and_cng_mixture(self) -> None:
        render, stub = load_animation_function()
        render(1500.0, "CNG", "Spark ignition")

        self.assertIn('aria-label="Spark plug"', stub.html)
        self.assertIn("SPARK PLUG", stub.html)
        self.assertIn("AIR + CNG", stub.html)
        self.assertIn("Spark ignition + expansion", stub.html)
        self.assertNotIn('aria-label="Fuel injector"', stub.html)


if __name__ == "__main__":
    unittest.main()
