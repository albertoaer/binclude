# Binclude

A tool to link executables to a folder in the PATH

The purpose is to have a practical way to add a program to the PATH an invoke it or remove it from the PATH without modifying the PATH

The CLI is generated using [Fire](https://github.com/google/python-fire)

The only requisite is to have python accesible from the PATH of the terminal you want to invoke it, also available for GUI using pythonw

## How to use it

You must have a folder added to the PATH

Code this in the local binclude folder:

```
python main.py init <PATH>
```

Then you can access everywhere binclude:

```
binclude --help
```