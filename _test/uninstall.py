
# regular imports
import os
import sys
sys.path.insert(1, '../')

# local imports
from Installerator.uninstallerator import Uninstallerator # noqa E402 (ignore import order)

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # create an instance of the class
    uninstallerator = Uninstallerator()

    # get path to conf file
    src_dir = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(src_dir, 'uninstall.json')

    # run the instance
    uninstallerator.run(conf_path)
