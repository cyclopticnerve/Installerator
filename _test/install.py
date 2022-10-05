
# regular imports
import os
import sys
sys.path.insert(1, '../')

# local imports
from Installerator.installerator import Installerator # noqa E402 (ignore import order)

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # create an instance of the class
    installerator = Installerator()

    # get path to conf file
    src_dir = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(src_dir, 'install.json')

    # run the instance
    installerator.run(conf_path)
