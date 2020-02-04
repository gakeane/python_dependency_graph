"""

"""

import logging

from local import Local
from load import GitHub
from load import DirectoryParser
from parse import PythonFileParser

from data import parse_user_input
from logger import setup_logs

from pprint import pprint as pp

log = logging.getLogger()


def main():
    """

    """

    try:

        # parse the user input
        perferences = parse_user_input()

        # initialise the logs
        setup_logs(perferences['verbose'])

        # clone into a git repository if provided
        if perferences['repository']:
            GitHub.clone(perferences['repository'], perferences['local_dir'])

        # locate all the python files in the repository
        files = DirectoryParser().get_python_files(perferences['local_dir'], perferences['ignore_list'])

        # run the python file parser to determine imports, modules and dependencies
        modules, imports = PythonFileParser().parse(files)

        pp(modules)
        pp(imports)

    finally:
        # Local.delete_directory('tmp_git_repo')
        pass

if __name__ == "__main__":
    main()
