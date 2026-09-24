"""Smoke test for the Streamlit user interface."""

import unittest

from streamlit.testing.v1 import AppTest


class StreamlitAppTests(unittest.TestCase):
    def test_default_app_loads_without_exception(self) -> None:
        app = AppTest.from_file("../app.py", default_timeout=30)
        app.run()

        self.assertEqual(list(app.exception), [])
        self.assertEqual(len(app.tabs), 3)
        self.assertGreaterEqual(len(app.sidebar.number_input), 5)
        self.assertEqual(len(app.sidebar.selectbox), 1)


if __name__ == "__main__":
    unittest.main()
