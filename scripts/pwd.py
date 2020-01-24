"""
This command returns the current directory
"""
import os

def run(*args):
    yield os.getcwd()
