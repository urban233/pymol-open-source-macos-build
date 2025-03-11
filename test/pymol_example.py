import pathlib

from pymol import cmd

_FILEPATH = pathlib.Path(__file__).parent


if __name__ == '__main__':
    cmd.fetch("3bmp")
    if pathlib.Path(_FILEPATH / "3bmp.cif").exists():
        print("Test failed!")
        print("The fetched protein could NOT be found!")
        exit(1)
    elif cmd.get_model("3bmp").atom[0].model != "3bmp":
        print("Test failed!")
        print("The fetched protein could NOT be found in the current PyMOL session!")
        exit(1)
    else:
        print("Test was successful.")
