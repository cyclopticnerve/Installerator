
# global imports
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# src = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, src)

# local imports
from uninstallerator import Uninstallerator # noqa E402 (ignore import order)

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
    ],
    "files": {
    },
    "postflight": [
    ]
}
# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # create an instance of the class
    uninstallerator = Uninstallerator()

    # # run the instance
    uninstallerator.run(dict_user)