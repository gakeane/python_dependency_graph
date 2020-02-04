
"""
Module containing tests for confirming corrcet operation of the dependency graph tool and it's utilities
"""

import os
import sys

sys.path.append("../src")

from local import Local
from load import GitHub
from load import DirectoryParser
from parse import PythonFileParser

import unittest

GIT_REPO = "https://github.com/gakeane/python_dependency_graph"
LOCAL_DIR = "tmp_dir"

PYTHON_FILES = ['data.py', 'load.py', 'local.py', 'logger.py', 'main.py', 'parse.py']
ADDITIONAL_FILES = ['.pylint' 'data.pyc', 'local.txt', 'main.py~']

PYTHON_CODE1 = """

import os
import re, sys

import logging.config

import matplotlib.pyplot as plt

def import_stuff():
    pass

"""

PYTHON_CODE2 = """

from src.local import Local
from load import GitHub

from src.load import DirectoryParser as DP

def get_all_imports():

    from parse import PythonFileParser

    pass

"""

class TestDependencyGraph(unittest.TestCase):
    """

    """

    def test_clone_from_github(self):
        """ Confirms we can clone from a repository on GitHub """

        try:
            Local.create_directory(LOCAL_DIR)
            GitHub.clone(GIT_REPO, LOCAL_DIR)

            self.assertTrue(Local.dir_exists(os.path.join(LOCAL_DIR, 'python_dependency_graph')))
        finally:
            Local.delete_directory(LOCAL_DIR)

    def test_get_all_python_files(self):
        """ Confirms that we identify all python files for a provided directory """
        try:
            Local.create_directory(LOCAL_DIR)
            Local.create_directory(os.path.join(LOCAL_DIR, 'subdir_1'))
            Local.create_directory(os.path.join(LOCAL_DIR, 'subdir_2'))

            for py_file in PYTHON_FILES:
                with open(os.path.join(LOCAL_DIR, 'subdir_1', py_file), 'w') as f:
                    pass

            for txt_file in ADDITIONAL_FILES:
                with open(os.path.join(LOCAL_DIR, 'subdir_2', txt_file), 'w') as f:
                    pass

            python_file_paths = DirectoryParser().get_python_files(LOCAL_DIR)
            python_files = [os.path.split(path)[1] for path in python_file_paths]

            self.assertEqual(python_files, PYTHON_FILES)

        finally:
            Local.delete_directory(LOCAL_DIR)

    def test_get_module_imports(self):
        """ Confirms we get all imports contained within a python module """

        try:
            Local.create_directory(LOCAL_DIR)

            with open(os.path.join(LOCAL_DIR, 'file1.py'), 'w') as f:
                f.write(PYTHON_CODE1)

            with open(os.path.join(LOCAL_DIR, 'file2.py'), 'w') as f:
                f.write(PYTHON_CODE2)

            python_files = [os.path.join(LOCAL_DIR, 'file1.py'), os.path.join(LOCAL_DIR, 'file2.py')]
            all_imports = PythonFileParser().parse(python_files)

        finally:
            Local.delete_directory(LOCAL_DIR)


if __name__ == "__main__":
    unittest.main()
