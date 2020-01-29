# pysh
A simple command line shell written in python

### About
This utility provides a simple shell that runs python scripts and python code instead of typical shell commands. The purpose of this utility is to help those new to the command line better understand what a shell is, how a $PATH works, and various other aspects of using the command line.

### How It Works
PySH accepts lines of user input and parses them as commands. The first word of each line is treated as the command name, and PySH searches $PYSH_PATH for directories containg a .py file matching that command. If a file matching the command is found and contains a *run()* method, PySH will execute that *run()* method passing the remainder of the line as method parameters.

![image](https://i.imgur.com/KuRlhYY.png)

### Installation
1. Install [python3](https://www.python.org/downloads/)
2. Clone repository
3. Run `python3 pysh.py`

### Extending
To add more commands, simply add .py files to any of the directories in $PYSH_PATH. The file should contain a *run()* or a *run(\*args)* method. That method will be executed whenever the command is typed. A few example scripts are provided.
