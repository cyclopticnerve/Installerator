#!/usr/bin/env python3
# -----------------------------------------------------------------------------#
# Filename: install.py                                           /          \  #
# Project : Installer                                           |     ()     | #
# Date    : 09/29/2022                                          |            | #
# Author  : Dana Hynes                                          |   \____/   | #
# License : WTFPLv2                                              \          /  #
# -----------------------------------------------------------------------------#

# NEXT: cmdline option for path to config file
# NEXT: less output, only print step name and ... Done
# NEXT: pre/postflight exit codes
# NEXT: unattended install to get rid of messages - need to select [Y/n]
# NEXT: how to check results of apt and pip install
#       use subprocess.call and check result - see main script
#       wrap in helper function __run()
# NEXT: redirect apt and pip to /dev/null to reduce messages
# NEXT: make a module with installer/uninstaller
# NEXT: add version string to options and print at start of install

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import json
import os
import shlex
import shutil
import subprocess

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 1

# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------


class Installer:

    # --------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self):

        # get locations
        self.src_dir = os.path.dirname(os.path.abspath(__file__))
        self.conf_path = os.path.join(self.src_dir, 'install.json')

        # set default config dict
        self.conf_dict_def = {
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

        # user config dict (set to defaults before trying to load file)
        self.conf_dict = self.conf_dict_def.copy()

    # --------------------------------------------------------------------------
    # Run the script
    # --------------------------------------------------------------------------
    def run(self):

        # init the config dict from user settings
        self.__load_conf()

        # substitute ${HOME} in config file
        self.__make_subs()

        # check if we need sudo password
        self.__check_sudo()

        # show some text
        prog_name = self.conf_dict['general']['prog_name']
        print(f'Installing {prog_name}')

        # do the steps in order
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
    # Run preflight scripts
    # --------------------------------------------------------------------------

    def do_preflight(self):

        # check for empty/no list
        if not (self.__needs_step('preflight')):
            return

        # show some text
        print('Running preflight scripts')

        for item in self.conf_dict['preflight']:

            # show that we are doing something
            print(f'Running {item}')

            # make relative file into absolute
            abs_item = os.path.join(self.src_dir, item)

            # run item
            cmd = abs_item
            cmd_array = shlex.split(cmd)
            try:
                if not DEBUG:
                    subprocess.run(cmd_array)
                else:
                    print(f'DEBUG: {cmd}')
            except Exception as error:
                print(f'Could not run {cmd}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Install system prerequisites
    # --------------------------------------------------------------------------
    def do_sys_reqs(self):

        # check for empty/no list
        if not (self.__needs_step('sys_reqs')):
            return

        # show some text
        print('Installing system requirements')

        # get system requirements
        for item in self.conf_dict['sys_reqs']:

            # show that we are doing something
            print(f'Installing {item}')

            # install apt reqs
            cmd = f'sudo apt-get install {item}'
            cmd_array = shlex.split(cmd)
            try:
                if not DEBUG:
                    cp = subprocess.run(cmd_array)
                    cp.check_returncode()
                else:
                    print(f'DEBUG: {cmd}')
            except Exception as error:
                print(f'Could not install {item}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Install python prerequisites
    # --------------------------------------------------------------------------
    def do_py_reqs(self):

        # check for empty/no list
        if not (self.__needs_step('py_reqs')):
            return

        # show some text
        print('Installing python requirements')

        # show that we are doing something
        print('Installing pip')

        # always install pip
        cmd = 'sudo apt-get install python3-pip'
        cmd_array = shlex.split(cmd)
        try:
            if not DEBUG:
                cp = subprocess.run(cmd_array)
                cp.check_returncode()
            else:
                print(f'DEBUG: {cmd}')
        except Exception as error:
            print(f'Could not install pip: {error}')
            exit()

        # get python requirements
        for item in self.conf_dict['py_reqs']:

            # show that we are doing something
            print(f'Installing {item}')

            # install pip reqs
            cmd = f'pip3 install {item}'
            cmd_array = shlex.split(cmd)
            try:
                if not DEBUG:
                    cp = subprocess.run(cmd_array)
                    cp.check_returncode()
                else:
                    print(f'DEBUG: {cmd}')
            except Exception as error:
                print(f'Could not install {item}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Make any necessary directories
    # --------------------------------------------------------------------------
    def do_dirs(self):

        # check for empty/no list
        if not (self.__needs_step('dirs')):
            return

        # show some text
        print('Creating directories')

        # for each folder we need to make
        for item in self.conf_dict['dirs']:

            # show that we are doing something
            print(f'Creating directory {item}')

            # make the folder(s)
            try:
                if not DEBUG:
                    os.makedirs(item, exist_ok=True)
                else:
                    print(f'DEBUG: {item}')
            except Exception as error:
                print(f'Could not create directory {item}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Copy all files to their dests
    # --------------------------------------------------------------------------
    def do_files(self):

        # check for empty/no list
        if not (self.__needs_step('files')):
            return

        # show some text
        print('Copying files')

        # for each file we need to copy
        for key, val in self.conf_dict['files'].items():

            # show that we are doing something
            print(f'Copying {key} to {val}')

            # convert relative path to absolute path
            abs_key = os.path.join(self.src_dir, key)

            # copy the file
            try:
                if not DEBUG:
                    shutil.copy(abs_key, val)
                else:
                    print(f'DEBUG: {abs_key} : {val}')
            except Exception as error:
                print(f'Could not copy file {abs_key}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Run postflight scripts
    # --------------------------------------------------------------------------
    def do_postflight(self):

        # check for empty/no list
        if not (self.__needs_step('postflight')):
            return

        # show some text
        print('Running postflight scripts')

        for item in self.conf_dict['postflight']:

            # show that we are doing something
            print(f'Running {item}')

            # make relative file into absolute
            abs_item = os.path.join(self.src_dir, item)

            # run item
            cmd = abs_item
            cmd_array = shlex.split(cmd)
            try:
                if not DEBUG:
                    subprocess.run(cmd_array)
                else:
                    print(f'DEBUG: {cmd}')
            except Exception as error:
                print(f'Could not run {cmd}: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Helpers
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Load dictionary data from a file
    # --------------------------------------------------------------------------
    def __load_conf(self):

        # make sure the file exists
        if not os.path.exists(self.conf_path):
            print('Could not find config file')
            exit()

        # read config file
        with open(self.conf_path, 'r') as file:
            try:
                self.conf_dict = json.load(file)

                # make sure we have minimum keys
                self.__merge_conf_dicts(self.conf_dict_def, self.conf_dict)
            except Exception as error:
                print(f'could not load config file: {error}')
                exit()

    # --------------------------------------------------------------------------
    # Perform substitutions for paths in config file
    # --------------------------------------------------------------------------
    def __make_subs(self):

        # get current user's home dir
        home_dir = os.path.expanduser('~')

        # the dict of substitutions
        sub_dict = {
            '${HOME}': home_dir
        }

        # create a temporary dict (can't modify conf_dict while iterating)
        tmp_dict = self.conf_dict.copy()

        # for each section in the conf dict
        for sect_name, sect_dict in tmp_dict.items():

            # if it's a list
            if isinstance(sect_dict, list):

                # empty the target list
                self.conf_dict[sect_name] = []

                # for each item
                for item in sect_dict:

                    # assume unchanged
                    tmp_item = item

                    # if it's a string
                    if isinstance(item, str):

                        # do the substitution
                        for sub_key, sub_val in sub_dict.items():
                            tmp_item = tmp_item.replace(sub_key, sub_val)

                    # modify user list
                    self.conf_dict[sect_name].append(tmp_item)

            # if it's a dict
            elif isinstance(sect_dict, dict):

                # for each kv pair in dict
                for key, val in sect_dict.items():

                    # assume unchanged
                    tmp_val = val

                    # if the val is a string
                    if isinstance(val, str):

                        # do the substitution
                        for sub_key, sub_val in sub_dict.items():
                            tmp_val = tmp_val.replace(sub_key, sub_val)

                    # modify user dict
                    self.conf_dict[sect_name][key] = tmp_val

    # --------------------------------------------------------------------------
    # Check if we are going to need sudo password and get it now
    # --------------------------------------------------------------------------
    def __check_sudo(self):

        # if either of theses steps is required, we need sudo
        if self.__needs_step('sys_reqs') or self.__needs_step('py_reqs'):

            # ask for sudo password now
            cmd = 'sudo echo -n'
            cmd_array = shlex.split(cmd)
            subprocess.run(cmd_array)

    # --------------------------------------------------------------------------
    # Check if a step needs to be performed or can be skipped
    # --------------------------------------------------------------------------
    def __needs_step(self, step):

        # if the section is present
        if step in self.conf_dict.keys():
            conf_dict = self.conf_dict[step]

            # if there are entries in the section
            if len(conf_dict):
                return True

        # otherwise we can skip this step
        return False

    # --------------------------------------------------------------------------
    # Merge required keys from def dict to user dict
    # --------------------------------------------------------------------------
    def __merge_conf_dicts(self, dict_src, dict_dst, path=''):

        # if types match
        if type(dict_src) == type(dict_dst):

            # if both dicts
            if isinstance(dict_src, dict):
                for key in dict_src.keys():

                    # if key in src but not dest
                    if key not in dict_dst.keys():

                        # just copy the whole key/value
                        dict_dst[key] = dict_src[key]

                    # key is in both
                    else:

                        # recurse to next level for matching
                        path = path + '/' + key
                        self.__merge_conf_dicts(dict_src[key], dict_dst[key], 
                                                path)

            # if both lists
            elif isinstance(dict_src, list):
                for item in dict_src:

                    # if item in src but not dst
                    if item not in dict_dst:

                        # add to dst
                        dict_dst.append(item)

        # dict/list mismatch
        else:
            raise Exception(f'Merge type mismatch: {path}')

# def __run(self, cmd=''):
#     try:
#         cp = subprocess.run(shlex.split(cmd), check=True)
#     except CalledProcessError as error:
#         pass


# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    installer = Installer()
    installer.run()

# -)
