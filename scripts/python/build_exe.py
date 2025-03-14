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
import os
import pathlib
import shutil
import zipfile
import platform
import subprocess

from cx_Freeze import Freezer, Executable


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

FILE_ROOT_PATH = pathlib.Path(__file__).parent


# Define the entry point of your application
executable = Executable(
  script="pymol/__init__.py",  # Replace with your script name
  target_name="Open-Source-PyMOL",  # Optional: Set the name of the .exe file
  #base="Win32GUI",  # Uncomment to suppress command window
  icon=pathlib.Path(FILE_ROOT_PATH.parent / "alternative_design" / "logo.ico")
)

# Create a freezer instance
freezer = Freezer(
  executables=[executable],
  includes=[
    "encodings", "PyQt5.uic", "pymol.povray", "pymol.parser", "uuid"
  ],
  excludes=[],  # Exclude unnecessary modules
  include_files=[],  # Include additional files
  zip_exclude_packages=[]
)


def remove_dist_info_folders(directory: pathlib.Path):
  """
  Remove all folders ending with .dist-info from the specified directory.

  Args:
      directory (str): The path to the directory to search.
  """
  for root, dirs, files in os.walk(str(directory)):
    for dir_name in dirs:
      if dir_name.endswith(".dist-info"):
        dist_info_path = os.path.join(root, dir_name)
        shutil.rmtree(dist_info_path)


if __name__ == '__main__':
  tmp_python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
  tmp_shared_suffix = f".cpython-{tmp_python_version.replace('.', '')}-darwin.so"
  tmp_arch = get_mac_architecture()
  tmp_build_dir_name = f"exe.macosx-{tmp_arch}-{tmp_python_version}"
  freezer.freeze()
  with zipfile.ZipFile(pathlib.Path(f"{FILE_ROOT_PATH}/build/{tmp_build_dir_name}/lib/library.zip"), 'r') as zip_ref:
    zip_ref.extractall(pathlib.Path(f"{FILE_ROOT_PATH}/build/{tmp_build_dir_name}/lib"))
  if not pathlib.Path(const.PROJECT_ROOT_DIR / "src/python/pymol").exists():
    utils.copy_pymol_sources()
    _CMD_FROM_BUILD_DIR = pathlib.Path(const.PROJECT_ROOT_DIR / "cmake-build-release" / f"_cmd{tmp_shared_suffix}")
    if _CMD_FROM_BUILD_DIR.exists():
      shutil.copy(
        _CMD_FROM_BUILD_DIR,
        pathlib.Path(const.PROJECT_ROOT_DIR / "src/python/pymol" / f"_cmd{tmp_shared_suffix}")
      )
    else:
      print(f"Could not find _cmd{tmp_shared_suffix} for building the EXE file.")
  else:
    print("The src/python/pymol directory already exists, that might mean a self compiled _cmd module was built.")
  remove_dist_info_folders(pathlib.Path(FILE_ROOT_PATH / f"build/{tmp_build_dir_name}/lib"))
  shutil.copytree(
    str(pathlib.Path(FILE_ROOT_PATH / "pymol/wizard")),
    str(pathlib.Path(FILE_ROOT_PATH / f"build/{tmp_build_dir_name}/lib/pymol/wizard")),
    dirs_exist_ok=True
  )
  shutil.copytree(
    str(pathlib.Path(FILE_ROOT_PATH / "pymol/data/startup")),
    str(pathlib.Path(FILE_ROOT_PATH / f"build/{tmp_build_dir_name}/lib/pymol/data/startup")),
    dirs_exist_ok=True
  )
