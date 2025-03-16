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
import pathlib
import shutil
import subprocess

import toml

import const
import build_macos_exe

pyproject_toml = toml.load("pyproject.toml")
PROJECT_NAME = pyproject_toml["project"]["name"]
PROJECT_VERSION = pyproject_toml["project"]["version"]


def build_dmg():
  """Function that build the dmg based on the .app package."""
  build_macos_exe.build_using_setup_file()
  tmp_dist_app_package_path = pathlib.Path(const.PROJECT_ROOT_DIR / f"dist/Open-Source-PyMOL-{PROJECT_VERSION}.app")
  tmp_dmg_build_app_package_path = pathlib.Path(const.PROJECT_ROOT_DIR / f"tmp/Open-Source-PyMOL-{PROJECT_VERSION}.app")
  if not tmp_dist_app_package_path.exists():
    print(f"Could not find the dist/Open-Source-PyMOL-{PROJECT_VERSION}.app!")
    exit(1)

  shutil.copytree(tmp_dist_app_package_path, tmp_dmg_build_app_package_path,
                  dirs_exist_ok=True)
  subprocess.run(pathlib.Path(const.PROJECT_ROOT_DIR / f"scripts/shell/build_dmg.sh"))
  shutil.rmtree(tmp_dmg_build_app_package_path)
