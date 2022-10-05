#!/usr/bin/env python3
# -----------------------------------------------------------------------------#
# Filename: uninstallerator.py                                   /          \  #
# Project : Installerator                                       |     ()     | #
# Date    : 09/29/2022                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
# -----------------------------------------------------------------------------#

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# regular imports
import os
import shutil

# local imports
from Installerator.base_installerator import Base_Installerator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 1

# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------


class Uninstallerator(Base_Installerator):

    # --------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self):

        # base installer init
        super().__init__()

    # --------------------------------------------------------------------------
    # Run the script
    # --------------------------------------------------------------------------
    def run(self, conf_path):

        # base installer run
        super().run(conf_path)

        # show some text
        prog_name = self.dict_conf['general']['name']
        print(f'Uninstalling {prog_name}')

        self.do_preflight()
        self.do_dirs()
        self.do_files()
        self.do_postflight()

        # done uninstalling
        print(f'{prog_name} uninstalled')

    # --------------------------------------------------------------------------
    # Steps
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Delete any necessary directories
    # --------------------------------------------------------------------------
    def do_dirs(self):

        # check for empty/no list
        if not self.needs_step('dirs'):
            return

        # show some text
        print('Deleting directories')

        # for each folder we need to delete
        for item in self.dict_conf['dirs']:

            # show that we are doing something
            print(f'Deleting directory {item} ... ', end='')

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
    def do_files(self):

        # check for empty/no list
        if not self.needs_step('files'):
            return

        # show some text
        print('Deleting files')

        # for each file we need to delete
        for src, dst in self.dict_conf['files'].items():

            # show that we are doing something
            print(f'Deleting file {src} ... ', end='')

            # convert relative path to absolute path
            abs_src = os.path.join(dst, src)

            # delete the file (if it'wasn't in a folder above)
            if os.path.exists(abs_src):
                try:
                    if not DEBUG:
                        os.remove(abs_src)
                    print('Done')
                except Exception as error:
                    print('Fail')
                    print(f'Could not delete file {abs_src}: {error}')
                    exit()

# -)
