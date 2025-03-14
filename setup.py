"""
#A* -------------------------------------------------------------------
#B* This file contains source code for building the python package of
#-* the PyMOL computer program
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
import os
import pathlib
import shutil
import subprocess
import sys
import platform

from setuptools import find_packages
from setuptools import setup
from setuptools.command.build import build
from setuptools.command.build_ext import build_ext
from setuptools.command.install import install
import toml

pyproject_toml = toml.load("pyproject.toml")
PROJECT_NAME = pyproject_toml["project"]["name"]
PROJECT_VERSION = pyproject_toml["project"]["version"]

PROJECT_ROOT_DIR = pathlib.Path(__file__).parent
DEBUG = False  # Debug flag for not cleaning up certain build files.


def get_mac_architecture():
  try:
    # Get the hardware architecture using sysctl
    arch = subprocess.check_output(
      ['sysctl', '-n', 'hw.machine'],
      stderr=subprocess.DEVNULL
    ).decode().strip()
    return arch
  except subprocess.CalledProcessError:
    # Fallback to platform.machine() if sysctl isn't available (unlikely on macOS)
    return platform.machine()


class CMakeBuildExt(build_ext):
  """Custom command to build C++ extension using CMake."""

  def run(self):
    # Run the default build_ext command first
    build_ext.run(self)
    # Then trigger the CMake build
    self.build_cmake_extension()

  def build_cmake_extension(self):
    """Run CMake to build the C/C++ extension."""
    print(f"Architecture: {get_mac_architecture()}")
    tmp_python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    build_dir = os.path.join(".", "cmake-build-setup_py")
    os.makedirs(build_dir, exist_ok=True)

    tmp_cmd_suffix = f".cpython-{tmp_python_version.replace('.', '')}-darwin.so"

    # CMake arguments
    cmake_args = [
      "-DCMAKE_TOOLCHAIN_FILE=./vendor/vcpkg/scripts/buildsystems/vcpkg.cmake",
      f"-DPYTHON_VER={tmp_python_version}",
      f"-DSHARED_SUFFIX={tmp_cmd_suffix}",
      "-DCMAKE_OSX_ARCHITECTURES=arm64"
    ]

    # Run CMake to configure and build the extension
    subprocess.check_call(["cmake", PROJECT_ROOT_DIR] + cmake_args, cwd=build_dir)
    subprocess.check_call(["cmake", "--build", build_dir, "--config", "Release"])

    shutil.copyfile(
      pathlib.Path(
        PROJECT_ROOT_DIR / "cmake-build-setup_py" / f"_cmd{tmp_cmd_suffix}"
      ),
      pathlib.Path(
        PROJECT_ROOT_DIR / "src/python/pymol" / f"_cmd{tmp_cmd_suffix}"
      ),
    )


setup(
  name=PROJECT_NAME,  # Name of your package
  version=PROJECT_VERSION,
  packages=find_packages(where='src/python'),  # Looks for packages in src/python
  package_dir={'': 'src/python'},  # src/python as the root for packages
  package_data={"": ["*.*"], "pymol": ["*.*"]},
  ext_modules=[],  # Handled by CMake
  cmdclass={
    "build_ext": CMakeBuildExt
  },
  install_requires=[
    "numpy==1.26.4",
    "toml"
  ]
)
