import os

def run(*args):
    yield os.environ.get("USER")
