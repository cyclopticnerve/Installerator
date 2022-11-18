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

## Uninstalling

```python
python -m pip uninstall installerator
```

## -)