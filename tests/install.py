
# global imports
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# src = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, src)

# local imports

# 1
# from package.module import class
# from installerator.installerator import Installerator # noqa E402 (ignore import order)

# 2
import installerator # noqa E402 (ignore import order)

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

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # create an instance of the class
    # 1
    # inst = Installerator()
    # 2
    inst = installerator.installerator.Installerator()

    # # run the instance
    inst.run(dict_user)
