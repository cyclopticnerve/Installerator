# -----------------------------------------------------------------------------#
# Filename: uninstallerator.py                                   /          \  #
# Project : Installerator                                       |     ()     | #
# Date    : 09/29/2022                                          |            | #
# Author  : cyclopticnerve                                      |   \____/   | #
# License : WTFPLv2                                              \          /  #
# -----------------------------------------------------------------------------#

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
import os
import shutil

# local imports
from installerator.base_installerator import Base_Installerator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 0


# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------

class Uninstallerator(Base_Installerator):

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self):

        '''
            The default initialization of the class
        '''

        # base installer init
        super().__init__()

    # --------------------------------------------------------------------------
    # Run the script
    # --------------------------------------------------------------------------
    def run(self, dict_user):

        '''
            Runs the setup using the supplied user dictionary

            Paramaters:
                dict_user [dict]: the user dict to get options from
        '''

        # base installer run
        super()._run(dict_user)

        # show some text
        prog_name = self.dict_conf['general']['name']
        print(f'Uninstalling {prog_name}')

        super()._do_preflight()
        self._do_dirs()
        self._do_files()
        super()._do_postflight()

        # done uninstalling
        print(f'{prog_name} uninstalled')

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Delete any unnecessary directories
    # --------------------------------------------------------------------------
    def _do_dirs(self):

        '''
            Delete any specified directories
        '''

        # check for empty/no list
        if not super()._needs_step('dirs'):
            return

        # show some text
        print('Deleting directories')

        # for each folder we need to delete
        for item in self.dict_conf['dirs']:

            # show that we are doing something
            print(f'Deleting directory {item}... ', end='')

            # delete the folder
            try:
                if not DEBUG:
                    shutil.rmtree(item)
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not delete directory {item}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Delete any necessary files (outside above directiories)
    # --------------------------------------------------------------------------
    def _do_files(self):

        '''
            Delete any specified files
        '''

        # check for empty/no list
        if not super()._needs_step('files'):
            return

        # show some text
        print('Deleting files')

        # for each file we need to delete
        for src, dst in self.dict_conf['files'].items():

            # show that we are doing something
            print(f'Deleting file {src}... ', end='')

            # NB: removed because all paths should be absolute
            # convert relative path to absolute path
            # abs_src = os.path.join(dst, src)

            # delete the file (if it'wasn't in a folder above)
            if os.path.exists(src):
                try:
                    if not DEBUG:
                        os.remove(src)
                    print('Done')
                except Exception as error:
                    print('Fail')
                    print(f'Could not delete file {src}: {error}')
                    exit()

# -)
