
import os

from installer import Installer

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    installer = Installer()

    # get path to conf file
    src_dir = os.path.dirname(os.path.abspath(__file__))
    conf_path = os.path.join(src_dir, 'install.json')

    installer.run(conf_path)
