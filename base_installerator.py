#!/usr/bin/env python3
# -----------------------------------------------------------------------------#
# Filename: base_installerator.py                                /          \  #
# Project : Installerator                                       |     ()     | #
# Date    : 10/03/2022                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
# -----------------------------------------------------------------------------#

# NEXT: pre/postflight exit codes
# NEXT: cmdline option for path to config file
# NEXT: add version string to options and print at start of install
# NEXT: custom substitutions?
# TODO: which paths should be absolute/relative (json_format.txt)

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# regular imports
import os
import shlex
import subprocess

# local imports
from Installerator.Configurator.configurator import Configurator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 1

# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------


class Base_Installerator:

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self):

        # get location
        self.src_dir = os.path.dirname(os.path.abspath(__file__))

    # --------------------------------------------------------------------------
    # Run the script
    # --------------------------------------------------------------------------
    def run(self, conf_path):

        # get current user's home dir
        home_dir = os.path.expanduser('~')

        # the dict of substitutions
        dict_subs = {
            '${HOME}': home_dir,
            '${SRC}': self.src_dir
        }

        # the default dict dir
        dict_conf_defaults = {
            'general': {
                'prog_name':    ''
            },
            'preflight': [
            ],
            'sys_reqs': [
            ],
            'py_reqs': [
            ],
            'dirs': [
            ],
            'files': {
            },
            'postflight': [
            ]
        }

        # user config dict
        configurator = Configurator()
        try:
            self.dict_conf = configurator.load(conf_path, dict_conf_defaults,
                                               dict_subs)
        except Exception as error:
            print(error)
            exit()

    # --------------------------------------------------------------------------
    # Check if we are going to need sudo password and get it now
    # --------------------------------------------------------------------------
    def check_sudo(self):

        # if either of theses steps is required, we need sudo
        if self.needs_step('sys_reqs') or self.needs_step('py_reqs'):

            # ask for sudo password now
            cmd = 'sudo echo -n'
            cmd_array = shlex.split(cmd)
            subprocess.run(cmd_array)

    # --------------------------------------------------------------------------
    # Run preflight scripts
    # --------------------------------------------------------------------------
    def do_preflight(self):
        self.__run_scripts('preflight')

    # --------------------------------------------------------------------------
    # Run postflight scripts
    # --------------------------------------------------------------------------
    def do_postflight(self):
        self.__run_scripts('postflight')

    # --------------------------------------------------------------------------
    # Check if a step needs to be performed or can be skipped
    # --------------------------------------------------------------------------
    def needs_step(self, step):

        # if the section is present
        if step in self.dict_conf.keys():

            # if there are entries in the section
            dict_conf = self.dict_conf[step]
            if len(dict_conf):
                return True

        # otherwise we can skip this step
        return False

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run preflight/postflight scripts
    # --------------------------------------------------------------------------
    def __run_scripts(self, step):

        # check for empty/no list
        if not self.needs_step(step):
            return

        # show some text
        print(f'Running {step} scripts')

        for item in self.dict_conf[step]:

            # show that we are doing something
            print(f'Running {item} ... ', end='')

            # run item
            cmd_array = shlex.split(item)
            try:
                if not DEBUG:
                    subprocess.run(cmd_array)
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not run {item}: {error}')
                exit()

# -)
