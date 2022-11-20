# -----------------------------------------------------------------------------#
# Filename: base_installerator.py                                /          \  #
# Project : Installerator                                       |     ()     | #
# Date    : 10/03/2022                                          |            | #
# Author  : cyclopticnerve                                      |   \____/   | #
# License : WTFPLv2                                              \          /  #
# -----------------------------------------------------------------------------#

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
import os
import shlex
import subprocess

# local imports
import configurator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 0


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

        '''
            The default initialization of the class
        '''

        # do nothing
        pass

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the script
    # --------------------------------------------------------------------------
    def _run(self, dict_user):

        '''
            Runs the setup using the supplied user dictionary

            Paramaters:
                dict_user [dict]: the user dict to get options from
        '''

        # the defs dict
        dict_defs = {
            'general': {
                'name':    ''
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

        # get current user's home dir
        home_dir = os.path.expanduser('~')

        # get location
        src_dir = os.path.dirname(os.path.abspath(__file__))

        # the default dict of substitutions
        dict_subs = {
            '${HOME}': home_dir,
            '${SRC}': src_dir
        }

        # do the config merge
        self.dict_conf = configurator.load(dict_defs, dict_user, dict_subs)

    # --------------------------------------------------------------------------
    # Check if we are going to need sudo password and get it now
    # --------------------------------------------------------------------------
    def _check_sudo(self):

        '''
            Checks if we need sudo permission early in the install

            Returns:
                ret [bool]: True if we need sudo permission, False if we don't
        '''

        # if either of theses steps is required, we need sudo
        if self._needs_step('sys_reqs') or self._needs_step('py_reqs'):

            # ask for sudo password now
            cmd = 'sudo echo -n'
            cmd_array = shlex.split(cmd)
            subprocess.run(cmd_array)

    # --------------------------------------------------------------------------
    # Run preflight scripts
    # --------------------------------------------------------------------------
    def _do_preflight(self):

        '''
            Run preflight scripts (before we do the heavy lifting)
        '''

        # run preflight scripts
        self._run_scripts('preflight')

    # --------------------------------------------------------------------------
    # Run postflight scripts
    # --------------------------------------------------------------------------
    def _do_postflight(self):

        '''
            Run postflight scripts (after we do the heavy lifting)
        '''

        # run postflight scripts
        self._run_scripts('postflight')

    # --------------------------------------------------------------------------
    # Check if a step needs to be performed or can be skipped
    # --------------------------------------------------------------------------
    def _needs_step(self, step):

        '''
            Check if an entry in the defs/user needs to be run

            Paramaters:
                step [str]: the step to check for in the final dict

            Returns:
                ret [bool]:True if the dict contains the step, False otherwise
        '''

        # if the section is present
        if step in self.dict_conf.keys():

            # if there are entries in the section
            dict_conf = self.dict_conf[step]
            if len(dict_conf):
                return True

        # otherwise we can skip this step
        return False

    # --------------------------------------------------------------------------
    # Run preflight/postflight scripts
    # --------------------------------------------------------------------------
    def _run_scripts(self, step):

        '''
            Runs the scripts from preflight or postflight

            Paramaters:
                step [str]: The step to run, either preflight or postflight

            Returns:
                ret [int]: Not Implemented yet
        '''

        # check for empty/no list
        if not self._needs_step(step):
            return

        # show some text
        print(f'Running {step} scripts')

        for item in self.dict_conf[step]:

            # show that we are doing something
            print(f'Running {item}... ', end='')

            # run item
            cmd_array = shlex.split(item)
            try:
                if not DEBUG:
                    cp = subprocess.run(cmd_array, check=True)
                    cp.check_returncode()
                print('Done')
            except Exception as error:
                print('Fail')
                print(f'Could not run {item}: {error}')
                exit()

# -)
