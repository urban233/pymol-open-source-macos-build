import pathlib
import subprocess

import const


def run_pytest_suite():
  """Runs the pytest suite."""
  subprocess.run(
    [pathlib.Path(const.PROJECT_ROOT_DIR / ".venv/bin/pytest")],
    cwd=pathlib.Path(const.PROJECT_ROOT_DIR / "tests")
  )
