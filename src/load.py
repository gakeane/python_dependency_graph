"""
This is a simple module for handling cloning repositories from github
"""

import re
import logging

from local import Local

log = logging.getLogger()


class GitHub:
    """

    """

    def __init__(self):
        """

        """


    @staticmethod
    def clone(git_repo, local_repo):
        """ Creates a local directory to store the git repo, then clone the repo from github (or some other repository)

        """

        Local.create_directory(local_repo)
        Local.run_shell_cmd('git clone --depth 1 %s' % git_repo, working_dir=local_repo, shell=True)


class DirectoryParser:
    """

    """

    def __init__(self):
        """ initialises variables for storing all the python files in the repository

        """

        self.ignore_list = list()
        self.ignore_files = list()

        self.python_files = list()


    def get_python_files(self, root_dir, ignore_list=None):
        """ Returns a list of all the python files in a directory
        This method resursivly moves through each of the sub directories and finds all files with the .py extension

        """

        # this will only be performed on the first call
        if ignore_list:
            self.ignore_dirs, self.ignore_files = self._parse_ignore_list(ignore_list)

        sub_dirs, dir_files = Local.list_directory(root_dir)

        # find all python files in directory
        for dir_file in dir_files:
            if re.match('.*\.py$', dir_file):
                self.python_files.append(dir_file)

        # search all sub-directories
        for sub_dir in sub_dirs:
            self.get_python_files(sub_dir)

        return self.python_files


    #########################
    # PRIVATE METHODS
    #########################

    def _parse_ignore_list(self, ignore_list):
        """ Returns two lists, one of all the directories to be ignored and the other of all the python files
        It is assumed that any string ending in '.py' is a python file and everything else refers to a dircetory

        ignore_list (list): list of strings representing the names of directories or python files to be ignored
        """

        files = list()
        dirs = list()

        for item in ignore_list:
            if re.match('.*\.py$', item):
                files.append(item)
            else:
                dirs.append(item)

        return dirs, files
