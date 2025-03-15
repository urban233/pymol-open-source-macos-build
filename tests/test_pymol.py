"""
#A* -------------------------------------------------------------------
#B* This file contains source code for running a simple example
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

from pymol import cmd

_FILEPATH = pathlib.Path(__file__).parent


def test_fetch():
  cmd.fetch("3bmp")
  assert pathlib.Path(_FILEPATH / "3bmp.cif").exists() is True
  assert cmd.get_model("3bmp").atom[0].model == "3bmp"
