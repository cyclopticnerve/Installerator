# ------------------------------------------------------------------------------
# Project : Installerator                                          /          \
# Filename: installerator.py                                      |     ()     |
# Date    : 09/29/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
import os
import shlex
import shutil
import subprocess

# local imports
from installerator.base_installerator import Base_Installerator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 1


# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------

class Installerator(Base_Installerator):

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

        # check if we need sudo password
        super()._check_sudo()

        # show some text
        prog_name = self.dict_conf['general']['name']
        print(f'Installing {prog_name}')

        super()._do_preflight()
        self._do_sys_reqs()
        self._do_py_reqs()
        self._do_dirs()
        self._do_files()
        super()._do_postflight()

        # done installing
        print(f'{prog_name} installed')

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Install system prerequisites
    # --------------------------------------------------------------------------
    def _do_sys_reqs(self):

        '''
            Install any system requirements
        '''

        # check for pip necessary
        if super()._needs_step('py-reqs'):
            self.dict_conf['sys_reqs'].append('python3-pip')

        # check for empty/no list
        if not super()._needs_step('sys_reqs'):
            return

        # show some text
        print('Installing system requirements')

        # get system requirements
        for item in self.dict_conf['sys_reqs']:

            # show that we are doing something
            print(f'Installing {item}... ', end='')

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
    def _do_py_reqs(self):

        '''
            Install any Python requirements
        '''

        # check for empty/no list
        if not super()._needs_step('py_reqs'):
            return

        # show some text
        print('Installing python requirements')

        # get python requirements
        for item in self.dict_conf['py_reqs']:

            # show that we are doing something
            print(f'Installing {item}... ', end='')

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
    def _do_dirs(self):

        '''
            Create any required folders
        '''

        # check for empty/no list
        if not super()._needs_step('dirs'):
            return

        # show some text
        print('Creating directories')

        # for each folder we need to make
        for item in self.dict_conf['dirs']:

            # show that we are doing something
            print(f'Creating directory {item}... ', end='')

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
    def _do_files(self):

        '''
            Copy (or create) any required files
        '''

        # check for empty/no list
        if not super()._needs_step('files'):
            return

        # show some text
        print('Copying files')

        # for each file we need to copy
        for src, dst in self.dict_conf['files'].items():

            # show that we are doing something
            print(f'Copying {src} to {dst}... ', end='')

            # NB: removed because all paths should be absolute
            # convert relative path to absolute path
            # abs_src = os.path.join(self.src_dir, src)

            # copy the file
            try:
                if not DEBUG:
                    shutil.copy(src, dst)
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not copy file {src}: {error}')
                exit()

# -)
