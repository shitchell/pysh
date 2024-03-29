#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module provides a simple shell that runs python scripts
as commands. Commands are found in directories defined in the
environment variable $PYSH_PATH. If a file is found in one of
these directories with a filename matching the command name and
ending in ".py", that file is loaded. The command file should
implement a "run()" method to be executed.

The basic steps for running commands is as follows:
    1. Retrieve a line of input from the user
    2. Split the line by spaces
    3. Find a command file in $PYSH_PATH that matches the first word of the line
    4. Execute the "run()" method in the command file, passing the rest of the line as method parameters
    5. Display the output of the "run()" method to the user
    6. Rinse and repeat
"""

import os
import time
import shlex
import optparse
import importlib.machinery

try:
    import readline
except:
    try:
        import pyreadline as readline
    except:
        pass


def log(*args):
    if options.verbose:
        prefix = time.strftime("[%Y.%m.%d_%H.%M.%S]")
        print(prefix, *args)


class PySH:
    def __init__(self):
        pass

    @property
    def path(self):
        """Returns the list of directories in which to find commands"""
        return os.environ.get("PYSH_PATH") or ".:./scripts"

    @property
    def prompt(self):
        """Returns the prompt to display at the beginning of each line"""
        prompt = os.environ.get("PYSH_PROMPT") or ">>> "
        prompt = prompt.encode().decode("unicode_escape")
        return prompt

    def find_command(self, command):
        """Given a command name, tries to find a script in the path matching that command"""
        command_filename = command + ".py"
        for path in self.path.split(":"):
            # Look through every directory in the path
            try:
                # Find all files in each directory in the path
                log("searching in '%s' for '%s'" % (path, command_filename))
                filenames = os.listdir(path)
            except:
                continue
            for filename in filenames:
                # Determine if any of the filenames in each directory matches
                # the given command name and ends with ".py"
                if filename == command_filename:
                    filepath = os.path.join(path, filename)
                    log("found '%s'" % filepath)
                    return filepath

    def load_command(self, command):
        """Given a command name, attempts to load the run method for that command"""
        filepath = self.find_command(command)
        if filepath:
            # Once a module is imported, its contents are loaded into
            # memory. This prevents any changes to the module from
            # being loaded while the program is running. We use importlib
            # to effectively reload the command module every time the
            # command is run
            loader = importlib.machinery.SourceFileLoader(command, filepath)
            module = loader.load_module()
            return module.run

    def run(self):
        """Indefinitely loops and executes commands"""
        while True:
            line = input(self.prompt)
            line = shlex.split(line)
            if len(line) > 0:
                start = time.time()
                name = line[0]
                args = line[1:]
                log("executing '%s' with args %s" % (name, args))
                try:
                    func = self.load_command(name)
                except Exception as err:
                    # Return any errors loading the command
                    yield "pysh: %s: %s" % (name, str(err))
                    continue
                if func:
                    # If the command was found in the path, run it
                    log("run(%s)" % str(args)[1:-1])
                    try:
                        for output in func(*args):
                            yield output
                    except Exception as err:
                        yield "pysh: %s: %s" % (name, str(err))
                else:
                    yield "pysh: %s: command not found" % name
                duration = time.time() - start
                log("%s: command completed in %fs" % (name, duration))


if __name__ == "__main__":
    # Parse the command line options
    parser = optparse.OptionParser()
    parser.add_option(
        "-v",
        "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="Print information about command execution",
    )
    (options, optionargs) = parser.parse_args()

    # Create a new instance of pysh
    shell = PySH()
    # Run forever
    while True:
        try:
            for output in PySH().run():
                print(output)
        except KeyboardInterrupt:
            # If the user types ^C, print an extra line and continue looping
            print()
        except EOFError:
            # If the user types ^D, print an extra line and exit
            print()
            break
