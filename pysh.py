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
import shlex
import importlib
try:
	import readline
except:
	try:
		import pyreadline as readline
	except:
		pass

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
		return os.environ.get("PYSH_PROMPT") or ">>> "

	def find_command(self, command):
		"""Given a command name, tries to find a script in the path matching that command"""
		for path in self.path.split(":"):
			# Look through every directory in the path
			try:
				# Find all files in each directory in the path
				filenames = os.listdir(path)
			except:
				continue
			for filename in filenames:
				# Determine if any of the filenames in each directory matches
				# the given command name and ends with ".py"
				if filename == command + ".py":
					filepath = os.path.join(path, filename)
					return filepath

	def load_command(self, command):
		"""Given a command name, attempts to load the script file for that command"""
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
				name = line[0]
				args = line[1:]
				try:
					func = self.load_command(name)
				except Exception as err:
				    # Return any errors loading the command
					yield "pysh: %s: %s" % (name, str(err))
					continue
				if func:
					# If the command was found in the path, run it
					for output in func(*args):
						yield output
				else:
					yield "pysh: %s: command not found" % name

if __name__ == '__main__':
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
