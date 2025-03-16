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
import build_macos_wheel
import build_macos_exe
import build_macos_so
import build_macos_dmg
import run_pytest
import dev_env


AUTOMATION_TREE = {
  "setup": {
    "help": "Setup automations",
    "subcommands": {
      "dev-env": {
        "help": "Sets up the development environment",
        "func": dev_env.setup_dev_env
      }
    }
  },
  "build": {
    "help": "Build targets",
    "subcommands": {
      "wheel": {
        "help": "Builds the Python wheel file",
        "func": build_macos_wheel.build_wheel
      },
      "exe": {
        "help": "Creates a frozen Python application",
        "func": build_macos_exe.build
      },
      "app": {
        "help": "Creates a frozen Python application as macOS app package",
        "func": build_macos_exe.build_using_setup_file
      },
      "dmg": {
        "help": "Creates a a DMG file from the macOS app package",
        "func": build_macos_dmg.build_dmg
      },
      "so": {
        "help": "Compiles the _cmd module from source",
        "func": build_macos_so.build_cmd_module
      }
    }
  },
  "test": {
    "help": "Runs all tests under the tests/ directory using pytest.",
    "func": run_pytest.run_pytest_suite
  }
}


if __name__ == "__main__":
  from task_automator import automator
  automator.Automator(AUTOMATION_TREE).run()
