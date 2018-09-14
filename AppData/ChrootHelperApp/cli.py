#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Main command line application.

Attributes
----------
docopt_doc : str
    Used to store/define the docstring that will be passed to docopt as the "doc" argument.

    .. note::
        - If I use a doc string that complies with Sphinx/RST, docopt will not parse it correctly.
        - If I use a doc string that complies with docopt, Sphinx doesn't SHUT THE HELL UP about \
        incorrect indentations and the likes.
        - So, I store the "docopt document" in a variable. This will SHUT THE HELL UP Sphinx \
        because it "cannot see" the doc string. The variable then is explicitly passed to docopt \
        as the "doc" argument. Moving the hell on!!!

root_folder : str
    The main folder containing the application. All commands must be executed from this location
    without exceptions.
"""

import os
import sys

# from . import app_utils
from .__init__ import __appname__, __appdescription__, __version__, __status__
from .python_utils import exceptions, log_system, shell_utils, file_utils
from .python_utils.docopt import docopt

if sys.version_info < (3, 5):
    raise exceptions.WrongPythonVersion()

root_folder = os.path.realpath(os.path.abspath(os.path.join(
    os.path.normpath(os.getcwd()))))

# Store the "docopt" document in a variable to SHUT THE HELL UP Sphinx.
docopt_doc = """{__appname__} {__version__} {__status__}

{__appdescription__}

Usage:
    app.py mount (-p <partition> | --partition=<partition>)
                 [-m <target> | --mount-point=<target>]
    app.py unmount [-m <target> | --mount-point=<target>]
    app.py generate system_executable
    app.py (-h | --help | --version)

Options:

-h, --help
    Show this screen.

--version
    Show application version.

-p <partition>, --partition=<partition>
    The partition that one wants to mount to chroot into.
    Example: /dev/sda1

-m <target>, --mount-point=<target>
    The full path to a non-existent or empty directory that will be used to
    chroot into. If used with the `unmount` sub-command, it should be a path
    that was previously used with the `mount` sub-command.

""".format(__appname__=__appname__,
           __appdescription__=__appdescription__,
           __version__=__version__,
           __status__=__status__)


class CommandLineTool():
    """Command line tool.

    It handles the arguments parsed by the docopt module.

    Attributes
    ----------
    action : method
        Set the method that will be executed when calling CommandLineTool.run().
    logger : object
        See <class :any:`LogSystem`>.
    """

    def __init__(self, args):
        """
        Parameters
        ----------
        args : dict
            The dictionary of arguments as returned by docopt parser.
        """
        super(CommandLineTool, self).__init__()

        self.action = None
        file_utils.remove_surplus_files("UserData/logs", "CLI*")
        self.logger = log_system.LogSystem(filename=log_system.get_log_file(storage_dir="UserData/logs",
                                                                            prefix="CLI"),
                                           verbose=True)

        self.logger.info(shell_utils.get_cli_header(__appname__), date=False)
        print("")

        if args["generate"]:
            if args["system_executable"]:
                self.logger.info("System executable generation...")
                self.action = self.system_executable_generation

    def run(self):
        """Execute the assigned action stored in self.action if any.
        """
        if self.action is not None:
            self.action()

    def system_executable_generation(self):
        """See :any:`template_utils.system_executable_generation`
        """
        from .python_utils import template_utils

        template_utils.system_executable_generation(
            exec_name="chroot-helper-cli",
            app_root_folder=root_folder,
            sys_exec_template_path=os.path.join(
                root_folder, "AppData", "data", "templates", "system_executable"),
            bash_completions_template_path=os.path.join(
                root_folder, "AppData", "data", "templates", "bash_completions.bash"),
            logger=self.logger
        )


def main():
    """Initialize main command line interface.

    Raises
    ------
    exceptions.BadExecutionLocation
        Do not allow to run any command if the "flag" file isn't
        found where it should be. See :any:`exceptions.BadExecutionLocation`.
    """
    if not os.path.exists(".chroot-helper.flag"):
        raise exceptions.BadExecutionLocation()

    arguments = docopt(docopt_doc, version="%s %s" % (__appname__, __version__))
    print(arguments)
    # cli = CommandLineTool(arguments)
    # cli.run()


if __name__ == "__main__":
    pass
