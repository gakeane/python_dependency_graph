"""

"""


from local import Local

from load import GitHub
from load import DirectoryParser


from data import parse_user_input
from parse import PythonFileParser


from pprint import pprint as pp

def main():
    """

    """

    try:

        # parse the user input
        perferences = parse_user_input()

        # clone into a git repository if provided
        if perferences['repository']:
            GitHub.clone(perferences['repository'], perferences['local_dir'])

        # locate all the python files in the repository
        files = DirectoryParser().get_python_files(perferences['local_dir'], perferences['ignore_list'])

        # run the python file parser to determine imports
        parser = PythonFileParser()
        parser.parse(files)

        pp(parser.all_imports)

    finally:
        # Local.delete_directory('tmp_git_repo')
        pass

if __name__ == "__main__":
    main()
