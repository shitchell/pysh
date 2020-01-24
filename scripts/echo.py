"""
This command prints the given arguments
"""

def run(*args):
	line = " ".join(args)
	yield line
