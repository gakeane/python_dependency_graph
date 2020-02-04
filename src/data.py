"""
Module handles user input and passes the results the main program
Also displays help message for the Tool
"""

import argparse

TMP_GIT_REPO = 'tmp_git_repo'


def parse_user_input():
    """ Parse the aruments passed in on the command line

    """

    perferences = {'local_dir': None,
                   'ignore_list': None,
                   'repository': None,
                   'format': None,
                   'verbose': False,
                   'shell': False,
                   'view': True,
                   'clean': True}

    parser = argparse.ArgumentParser(description="Python Dependency Graph")

    parser.add_argument("-r", "--repository", type=str, dest="repository", default=None, help="URL to python git repository to be evaluated")
    parser.add_argument("-d", "--directory", type=str, dest="directory", default=None, help="Path to local python directory to be evaluated")
    parser.add_argument("-i", "--ignore-files", type=str, dest="ignore_files", default=None, help="Path to file containing list of ignore files/directories")
    parser.add_argument("-f", "--format", type=str, dest="graph_format", default="png", choices=['png', 'pdf'], help="The file type for dependency graph [png, pdf]")

    parser.add_argument("-v", "--verbose", action="store_true", default=False, help="increase output verbosity")
    parser.add_argument("-c", "--clean", action="store_false", default=True, help="If set won't clean temporary files or directories the tool creates")
    parser.add_argument("-s", "--shell", action="store_true", default=False, help="Git commands run from the default shell, (not recommended)")
    parser.add_argument("-vi", "--view", action="store_false", default=True, help="If set the dependecy graph will be rendered but not displayed")

    args = parser.parse_args()

    if args.repository:
        perferences['repository'] = args.repository
        perferences['local_dir'] = TMP_GIT_REPO

    elif args.directory:
        perferences['local_dir'] = args.directory

    else:
        raise ValueError("Must specify one of --repository or --directory")

    perferences['ignore_list'] = args.ignore_files
    perferences['format'] = args.graph_format

    perferences['verbose'] = args.verbose
    perferences['shell'] = args.shell
    perferences['view'] = args.view
    perferences['clean'] = args.clean

    return perferences
