"""
Usage: help [command]
This command provides a list of all commands in
$PYSH_PATH or provides help with a given command
"""

import os
import sys
import pysh

def run(*args):
    shell = pysh.PySH()
    if not args:
        for path in shell.path.split(":"):
            try:
                filenames = os.listdir(path)
            except:
                continue
            for filename in filenames:
                if filename.endswith(".py"):
                    command = filename[:-3]
                    try:
                        shell.load_command(command)
                    except:
                        continue
                    yield command
    else:
        func = shell.load_command(args[0])
        doc = sys.modules[func.__module__].__doc__.strip()
        if doc:
            yield doc
    