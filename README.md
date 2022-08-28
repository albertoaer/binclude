# Binclude

A tool to link executables to a folder in the PATH

The purpose is to have a practical way to add a program to the PATH an invoke it or remove it from the PATH without modifying the PATH

The CLI is generated using [Fire](https://github.com/google/python-fire)

## How to use it

You must already have a directory added to the PATH in order to work

Type this in the local binclude installation directory for initializing it
```
python main.py init <DIR>
```

The currently supported interpreters are python, bash, cmd and powershell

Once initiated you will be able to type in Bash, CMD and PowerShell consoles:
```ps
binclude --help
```

Some interpreters allow no extension, like python and bash, so the first in the list will be saved without extension and the other with extension. In the future will be configurable.

To include a file in the PATH use:
```
binclude add <FILE> <NAME> <INTERPRETER>
```
The interpreter is optional and is use for applications that needs an interpreter like python, ruby, etc, has nothing to do with the internal link interpreter representation commented before.