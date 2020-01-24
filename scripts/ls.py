import os
import glob

def run(*args):
	global filename

	if not args:
		# If no arguments are provided, list the contents of the current directory
		args = ["."]

	for arg in args:
		if not os.path.exists(arg):
			yield "%s: cannot access '%s': No such file or directory" % (filename, arg)
		elif not os.access(arg, os.R_OK):
			# Filepath is not readable
			yield "%s: cannot open '%s': Permission denied" % (filename, arg)
		elif os.path.isdir(arg):
			try:
				for filename in os.listdir(arg):
					filepath = os.path.join(arg, filename)
					if os.path.isdir(filepath):
						yield filename + os.path.sep
					else:
						yield filename
			except Exception as err:
				yield "%s: %s" % (filename, str(err))
		elif os.path.isfile(arg):
			yield filename

filename = os.path.basename(__file__).rstrip(".py")