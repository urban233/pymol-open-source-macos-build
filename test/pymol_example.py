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


if __name__ == '__main__':
    cmd.fetch("3bmp")
    if not pathlib.Path(_FILEPATH / "3bmp.cif").exists():
        print("Test failed!")
        print("The fetched protein could NOT be found!")
        exit(1)
    elif cmd.get_model("3bmp").atom[0].model != "3bmp":
        print("Test failed!")
        print("The fetched protein could NOT be found in the current PyMOL session!")
        exit(1)
    else:
        print("Test was successful.")
