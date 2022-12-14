# ------------------------------------------------------------------------------
# Project : Installerator                                          /          \
# Filename: __init__.py                                           |     ()     |
# Date    : 10/03/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

__version__ = "0.1.0"

"""
A small Python module that makes installing Python apps easier
"""

# import all modules in package to get full dot notation from package import
import installerator     # noqa W0611 (unused import)
import uninstallerator   # noqa W0611 (unused import)

# from <package_name> import *
__all__ = ["installerator", "uninstallerator"]

# -)
