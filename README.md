# siblink - a Python sibling package linker

![Version Badge](https://badgen.net/badge/version/1.2.2/blue?icon=github)

### Installation

```bash
pip install siblink
```

**OR**

```bash
git clone git@github.com:TreltaSev/siblink.git
cd ./siblink
pip install .
```

### Usage

`**siblink**` has some commands that you should familiarize yourself with, since siblink is built over with the [click](https://github.com/pallets/click) package, after installation, you can run

```bash
siblink --help
```

#### Usage

A package in pythons eyes is just a folder containing a `__init__.py` file, it makes variables easily discoverable between "packages". The way python knows what files it should make discoverable to you is through its built-in sys.path variable. `**siblink**` just adds a few more directories, the one behind your current directory, as well as every directory between the `.py` file and your working directory, which in turn, adds your current directories' siblings together.

Say you had two directories within the same directory.

```bash
parent
├───package_a
│       __init__.py
│
└───package_b
        main.py
```

the `__init__.py` file contains `some_variable`, you want to get that variable from main.py, if you attempt to run main.py normally, this would be your result.

```bash
python ./parent/package_b/main.py

Traceback (most recent call last):
  File ".\parent\package_b\main.py", line 1, in <module>
    import package_a
ModuleNotFoundError: No module named 'package_a'
```

You could always mutate the sys.path variable yourself but I've found that its annoying to do that if you have hundreds of files.

`**siblink**` automatically does this for you, now if you were to run main.py with `**siblink**`, this is your result.

```bash
siblink run ./parent/package_b/main.py

10
```
