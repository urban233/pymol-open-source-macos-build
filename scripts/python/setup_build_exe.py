import pathlib

from cx_Freeze import setup

PROJECT_ROOT_DIR = pathlib.Path(__file__).parent.parent
print(f"This is the project root dir setting currently: {PROJECT_ROOT_DIR}")


# Dependencies are automatically detected, but they might need fine-tuning.
build_exe_options = {
  "excludes": ["tkinter", "unittest"],
  "includes": ["copy", "encodings", "PyQt5.uic", "pymol.povray", "pymol.parser", "uuid"],
  "include_files": [
    (
      pathlib.Path(PROJECT_ROOT_DIR / ".venv/lib/python3.11/site-packages/pymol/_cmd.cpython-311-darwin.so"),
      "./lib/pymol/_cmd.cpython-311-darwin.so"
     )
  ]
}

setup(
  name="Open-Source-PyMOL",
  version="3.1.0a0",
  options={"build_exe": build_exe_options},
  executables=[
    {
      "target_name": "PyMOL",
      "script": pathlib.Path(PROJECT_ROOT_DIR / "pymol/pymol/startup_wrapper.py"),
      "base": "gui",
      "icon": pathlib.Path(PROJECT_ROOT_DIR / "alternative_design/icon.icns"),
    }
  ],
)
