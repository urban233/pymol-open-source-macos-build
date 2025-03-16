"""
#A* -------------------------------------------------------------------
#B* This file contains source code for running automation tasks related
#-* to the build process of the PyMOL computer program
#C* Copyright 2025 by Martin Urban.
#D* -------------------------------------------------------------------
#E* It is unlawful to modify or remove this copyright notice.
#F* -------------------------------------------------------------------
#G* Please see the accompanying LICENSE file for further information.
#H* -------------------------------------------------------------------
#I* Additional authors of this source file include:
#-*
#-*
#-*
#Z* -------------------------------------------------------------------
"""
import sys
import pathlib
import shutil
import subprocess

import const


class BuildMacOSExe:
  """Contains the logic for building the macOS EXE file."""

  def __init__(self) -> None:
    """Constructor."""
    self.src_path = pathlib.Path(const.PROJECT_ROOT_DIR / "pymol")
    self.pymol_data_path = pathlib.Path(const.PROJECT_ROOT_DIR / "pymol/pymol/data")
    self.build_script_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "pymol", "build_exe.py"
    )
    self.build_script_alt_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "pymol", "setup_build_exe.py"
    )
    self.license_filepath = pathlib.Path(const.PROJECT_ROOT_DIR / "pymol/LICENSE")
    self.readme_filepath = pathlib.Path(const.PROJECT_ROOT_DIR / "pymol/README.md")
    self.build_dir = pathlib.Path(const.PROJECT_ROOT_DIR / "pymol/build")

  def setup_build_environment(self) -> None:
    """Sets up a temporary build environment."""
    # <editor-fold desc="Path/Filepath definitions">
    tmp_build_script_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "scripts/python", "setup_build_exe.py"
    )
    tmp_vendor_pymol_path = pathlib.Path(
      const.PROJECT_ROOT_DIR / "vendor/pymol-open-source"
    )
    tmp_pymol_python_src_path = pathlib.Path(
      tmp_vendor_pymol_path / "modules"
    )
    tmp_pymol_data_path = pathlib.Path(
      tmp_vendor_pymol_path / "data"
    )
    tmp_pymol_license_filepath = pathlib.Path(
      tmp_vendor_pymol_path / "LICENSE"
    )
    tmp_pymol_readme_filepath = pathlib.Path(
      tmp_vendor_pymol_path / "README.md"
    )
    tmp_edited_pmg_qt_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "edited/pmg_qt" / "pymol_qt_gui.py"
    )
    tmp_edited_base_css_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "edited/pymol/data/pymol", "base.css"
    )
    tmp_edited_init_py_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "edited/pymol", "__init__.py"
    )
    tmp_edited_startup_wrapper_py_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "edited/pymol", "startup_wrapper.py"
    )
    tmp_alternative_splash_screen_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "alternative_design" / "splash.png"
    )
    # </editor-fold>
    # <editor-fold desc="Copy operations">
    shutil.copytree(tmp_pymol_python_src_path, self.src_path, dirs_exist_ok=True)
    shutil.copytree(tmp_pymol_data_path, self.pymol_data_path, dirs_exist_ok=True)
    shutil.copy(tmp_build_script_filepath, self.build_script_filepath)
    shutil.copy(tmp_pymol_license_filepath, self.license_filepath)
    shutil.copy(tmp_pymol_readme_filepath, self.readme_filepath)
    # <editor-fold desc="Custom file replacements">
    shutil.copy(
      tmp_edited_base_css_filepath,
      pathlib.Path(tmp_pymol_data_path / "pymol", "base.css")
    )
    shutil.copy(
      tmp_edited_pmg_qt_filepath,
      pathlib.Path(self.src_path / "pmg_qt", "pymol_qt_gui.py")
    )
    shutil.copy(
      tmp_edited_init_py_filepath,
      pathlib.Path(self.src_path / "pymol", "__init__.py")
    )
    shutil.copy(
      tmp_edited_startup_wrapper_py_filepath,
      pathlib.Path(self.src_path / "pymol", "startup_wrapper.py")
    )
    shutil.copy(
      tmp_alternative_splash_screen_filepath,
      pathlib.Path(self.src_path / "pymol/data/pymol", "splash.png")
    )
    # </editor-fold>
    # </editor-fold>

  def build(self) -> None:
    """Builds the PyMOL Windows EXE file."""
    self.setup_build_environment()
    subprocess.run(
      [const.PYTHON_EXECUTABLE, self.build_script_filepath],
      stdout=sys.stdout, stderr=sys.stderr, text=True, cwd=self.src_path
    )
    shutil.copytree(self.build_dir, pathlib.Path(const.PROJECT_ROOT_DIR / "dist"),
                    dirs_exist_ok=True)

  def setup_based_build(self) -> None:
    """Uses the cx_freeze setup.py for the build process."""
    self.setup_build_environment()
    tmp_build_script_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "scripts/python", "setup_build_exe.py"
    )
    shutil.copy(tmp_build_script_filepath, self.build_script_alt_filepath)
    tmp_edited_startup_wrapper_py_filepath = pathlib.Path(
      const.PROJECT_ROOT_DIR / "edited/pymol", "startup_wrapper.py"
    )
    shutil.copy(
      tmp_edited_startup_wrapper_py_filepath,
      pathlib.Path(self.src_path / "pymol", "startup_wrapper.py")
    )
    subprocess.run(
      [const.PYTHON_EXECUTABLE, self.build_script_alt_filepath, "bdist_mac"],
      stdout=sys.stdout, stderr=sys.stderr, text=True, cwd=self.src_path
    )
    shutil.copytree(self.build_dir, pathlib.Path(const.PROJECT_ROOT_DIR / "dist"),
                    dirs_exist_ok=True)


def build() -> None:
  """Builds the Windows EXE file using the BuildWinExe class."""
  tmp_build_macos_exe = BuildMacOSExe()
  tmp_build_macos_exe.build()


def build_using_setup_file():
  """Builds the EXE file but based on the setup.py for cx_freeze."""
  tmp_build_macos_exe = BuildMacOSExe()
  tmp_build_macos_exe.setup_based_build()
