"""
Module handles user input and passes the results the main program
"""

import argparse

TMP_GIT_REPO = 'tmp_git_repo'

def parse_user_input():
    """

    """

    perferences = {'local_dir': None,
                   'ignore_list': None,
                   'repository': None,
                   'verbose': False}

    parser = argparse.ArgumentParser(description="Python Dependency Graph")

    parser.add_argument("-r", "--repository", type=str, dest="repository", default=None, help="URL to python git repository to be evaluated")
    parser.add_argument("-d", "--directory", type=str, dest="directory", default=None, help="Path to local python directory to be evaluated")
    parser.add_argument("-i", "--ignore-files", type=str, dest="ignore_files", default=None, help="Path to file containing list of ignore files/directories")

    parser.add_argument("-v", "--verbose", action="store_true", help="increase output verbosity")

    args = parser.parse_args()

    if args.repository:
        perferences['repository'] = args.repository
        perferences['local_dir'] = TMP_GIT_REPO

    elif args.directory:
        perferences['local_dir'] = args.directory

    else:
        raise ValueError("Must specify one of --repository or --directory")

    if args.ignore_files:
        perferences['ignore_list'] = args.ignore_files

    if args.verbose:
        perferences['verbose'] = True

    return perferences
