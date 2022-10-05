#!/usr/bin/env python3
# -----------------------------------------------------------------------------#
# Filename: installerator.py                                     /          \  #
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
import shlex
import shutil
import subprocess

# local imports
from Installerator.base_installerator import Base_Installerator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 1

# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------


class Installerator(Base_Installerator):

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

        # check if we need sudo password
        self.check_sudo()

        # show some text
        prog_name = self.dict_conf['general']['name']
        print(f'Installing {prog_name}')

        self.do_preflight()
        self.do_sys_reqs()
        self.do_py_reqs()
        self.do_dirs()
        self.do_files()
        self.do_postflight()

        # done installing
        print(f'{prog_name} installed')

    # --------------------------------------------------------------------------
    # Steps
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Install system prerequisites
    # --------------------------------------------------------------------------
    def do_sys_reqs(self):

        # check for pip necessary
        if self.needs_step('py-reqs'):
            self.dict_conf['sys_reqs'].append('python3-pip')

        # check for empty/no list
        if not self.needs_step('sys_reqs'):
            return

        # show some text
        print('Installing system requirements')

        # get system requirements
        for item in self.dict_conf['sys_reqs']:

            # show that we are doing something
            print(f'Installing {item} ... ', end='')

            # install apt reqs
            cmd = f'sudo apt-get install {item} -qq > /dev/null'
            cmd_array = shlex.split(cmd)
            try:
                if not DEBUG:
                    cp = subprocess.run(cmd_array)
                    cp.check_returncode()
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not install {item}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Install python prerequisites
    # --------------------------------------------------------------------------
    def do_py_reqs(self):

        # check for empty/no list
        if not self.needs_step('py_reqs'):
            return

        # show some text
        print('Installing python requirements')

        # get python requirements
        for item in self.dict_conf['py_reqs']:

            # show that we are doing something
            print(f'Installing {item} ... ', end='')

            # install pip reqs
            cmd = f'pip3 install -q {item} > /dev/null'
            cmd_array = shlex.split(cmd)
            try:
                if not DEBUG:
                    cp = subprocess.run(cmd_array)
                    cp.check_returncode()
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not install {item}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Make any necessary directories
    # --------------------------------------------------------------------------
    def do_dirs(self):

        # check for empty/no list
        if not self.needs_step('dirs'):
            return

        # show some text
        print('Creating directories')

        # for each folder we need to make
        for item in self.dict_conf['dirs']:

            # show that we are doing something
            print(f'Creating directory {item} ... ', end='')

            # make the folder(s)
            try:
                if not DEBUG:
                    os.makedirs(item, exist_ok=True)
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not create directory {item}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Copy all files to their dests
    # --------------------------------------------------------------------------
    def do_files(self):

        # check for empty/no list
        if not self.needs_step('files'):
            return

        # show some text
        print('Copying files')

        # for each file we need to copy
        for src, dst in self.dict_conf['files'].items():

            # show that we are doing something
            print(f'Copying {src} to {dst} ... ', end='')

            # convert relative path to absolute path
            abs_src = os.path.join(self.src_dir, src)

            # copy the file
            try:
                if not DEBUG:
                    shutil.copy(abs_src, dst)
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not copy file {abs_src}: {error}')
                exit()

# -)
