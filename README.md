<!----------------------------------------------------------------------------->
<!-- Filename: README.md                                       /          \  -->
<!-- Project : Installerator                                   |     ()     | -->
<!-- Date    : 10/31/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Installerator

## "It mostly works™"

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

A small Python module that makes working with json settings files easier

## Installing

You can download the (hopefully stable) 
[latest release](https://github.com/cyclopticnerve/installerator/releases/latest) 
from the main branch. <br>
Download the Source Code (tar.gz) file. <br>
Then install it using:
```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ python -m pip install Installerator-X.X.X.tar.gz
```

Or you can clone the git repo to get the latest (and often broken) code from the dev branch:
```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/Installerator
foo@bar:~/Downloads$ cd Installerator
foo@bar:~/Downloads/Installerator$ python -m build
foo@bar:~/Downloads/Installerator$ python -m pip install ./dist/installerator-X.X.X.tar.gz -r ./requirements.txt
```

## Requirements

This package relies on another package, Configurator.
Find out more about this package [here](https://github.com/cyclopticnerve/configurator).

## Uninstalling

```python
python -m pip uninstall installerator
```

## Usage

### Install:
```python
# NB: the whole import thing is still hazy to me, but this works 100%
# from <package>.<module> import <Class>
from installerator.installerator import Installerator

# the user dict
dict_user = {
    "general": {
        "name": "SpaceOddity"
    },
    "py_reqs": [
        "python-crontab"
    ],
    "dirs": [
        "${HOME}/.spaceoddity",
        "${HOME}/.config/spaceoddity"
    ],
    "files": {
        "${SRC}/spaceoddity.py": "${HOME}/.spaceoddity",
        "${SRC}/LICENSE": "${HOME}/.spaceoddity",
        "${SRC}/VERSION": "${HOME}/.spaceoddity",
        "${SRC}/uninstall.py": "${HOME}/.spaceoddity",
        "${SRC}/uninstall.json": "${HOME}/.spaceoddity",
        "${SRC}/cron_uninstall.py": "${HOME}/.spaceoddity"
    },
    "postflight": [
        "${SRC}/convert_json.py",
        "${SRC}/cron_install.py",
        "${HOME}/.spaceoddity/spaceoddity.py"
    ]
}

# create an instance of the class
inst = Installerator()

# # run the instance
inst.run(dict_user)
```

### Uninstall:
```python
# NB: the whole import thing is still hazy to me, but this works 100%
# from <package>.<moule> import <Class>
from installerator.uninstallerator import Uninstallerator 

dict_user = {
    "general": {
        "name": "SpaceOddity"
    },
    "preflight": [
        "${HOME}/.spaceoddity/cron_uninstall.py"
    ],
    "dirs": [
        "${HOME}/.spaceoddity",
        "${HOME}/.config/spaceoddity"
    ]
}

# create an instance of the class
uninst = Uninstallerator()

# # run the instance
uninst.run(dict_user)
```

## -)
