<!----------------------------------------------------------------------------->
<!-- Project : Installerator                                   /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 10/31/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Installerator

## "It mostly works™"

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

A small Python module that makes installing Python apps easier

## Requirements

This package relies on another package, Configurator.
Find out more about this package [here](https://github.com/cyclopticnerve/configurator).

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
foo@bar:~$ python -m pip install build
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/Installerator
foo@bar:~/Downloads$ cd Installerator
foo@bar:~/Downloads/Installerator$ python -m build
foo@bar:~/Downloads/Installerator$ python -m pip install ./dist/installerator-X.X.X.tar.gz -r ./requirements.txt
```

## Uninstalling

```python
python -m pip uninstall installerator
```

## Usage

### Install.py:
```python

# from <package>.<module> import <Class>
from installerator.installerator import Installerator

# NB: configurator's dict_def and dict_subs are hard coded
# so the only thing we need is dict_user

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

### Uninstall.py:
```python

# from <package>.<moule> import <Class>
from installerator.uninstallerator import Uninstallerator 

# NB: configurator's dict_def and dict_subs are hard coded
# so the only thing we need is dict_user

# the user dict
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

## Notes

Currently, dict_defs and dict_subs are hard-coded to waht the lib expects. This
may change in future releases.
The dict_def looks like this (note which keys are dicts, and which are arrays):
```python
dict_defs = {
    'general': {
        'name':    ''
    },
    'preflight': [
    ],
    'sys_reqs': [
    ],
    'py_reqs': [
    ],
    'dirs': [
    ],
    'files': {
    },
    'postflight': [
    ]
}
```
And the dict_subs looks like this:
```python
# get current user's home dir
home_dir = os.path.expanduser('~')

# get location
src_dir = os.path.dirname(os.path.abspath(__file__))

# the default dict of substitutions
dict_subs = {
    '${HOME}': home_dir,
    '${SRC}': src_dir
}
```

## -)
