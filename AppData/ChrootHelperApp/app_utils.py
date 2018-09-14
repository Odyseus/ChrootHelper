#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Summary

Attributes
----------
root_folder : str
    The main folder containing the Knowledge Base. All commands must be executed
    from this location without exceptions.
sudo : str
    Path to sudo command.
"""

import os

from .python_utils import cmd_utils


root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.getcwd()))))


sudo = cmd_utils.which("sudo")

if sudo is None:
    raise Exception()

if __name__ == "__main__":
    pass
