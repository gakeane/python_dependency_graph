"""
Module for handling system administration on the local host.
This was tested and developed on a linux host.
Further work may be required for correct operation on a windows or other non-NIX hosts

"""

import subprocess
import os
import shutil
import shlex
import logging

log = logging.getLogger()


class Local:
    """

    """

    def __init__():
        """
        This is a static class so there is nothing to initialise here
        """

    @staticmethod
    def run_shell_cmd(cmd, stdin=None, working_dir=None, env_vars=None, check_result=True, shell=False):
        """ Executes a shell command (command is executed as a subprocess of the current python script)

        The process is started when we call Popen.
        Communicate allows us to send data to stdin and read from stdout and stderr, communicate will block until the command completes.

        cmd          (string):  The command to be executed
        stdin        (string):  Any input which needs to be passed to the subprocess (None if no input required)
        working_dir  (string):  The directory the shell command will be executed in (None to use python ROOT directory)
        env_vars     (dict):    Any environment variables to be set in the shell context for the subprocess (None to use current environment)
        check_result (boolean): If True will throw a ValueError if the command fails
        shell        (boolean): Setting the shell to true will run the command in the systems default shell (usually BASH on Linux and cmd.exe on windows).
                                This is generally considered a security risk so should not be enabled if not required.
                                It can be necessary to enable the shell for certain commands on windows as these commands don't have batch executables
        """

        cmd_list = shlex.split(cmd)

        if stdin:
            stdin = stdin.encode('utf-8')

        process = subprocess.Popen(cmd_list, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=working_dir, env=env_vars, shell=shell)
        stdout, stderr = process.communicate(input=stdin)

        if check_result and process.returncode != 0:
            raise ValueError("Command [%s] failed with the following standard error\n%s \n" % (cmd, stderr.decode('utf-8')))

        return process.returncode, stdout.decode('utf-8'), stderr.decode('utf-8')

    @staticmethod
    def file_exists(path):
        """ Returns True if specified path exists on the local machine and ends in a file

        path (string): The absolute/relative path we want to check i.e. "/usr/bin/test"
        """
        return os.path.isfile(path)

    @staticmethod
    def dir_exists(path):
        """ Returns True if specified path exists on the local machine and ends in a directory

        path (string): The absolute/relative path we want to check i.e. "/usr/bin/test"
        """
        return os.path.isdir(path)

    @staticmethod
    def create_directory(path):
        """
        This will create the specified directory if it does not already exist.
        If the directory does exists then it's contents will NOT be overwritten.
        All directories in the path will also be created if they do not already exist.

        path (string): The absolute/relative path of the directory we want to create i.e. "/usr/bin/test"
        """

        if not Local.dir_exists(path):

            if Local.file_exists(path):
                raise IOError("Path [%s] already exists as a file" % path)

            os.makedirs(path)

    @staticmethod
    def delete_directory(path):
        """ Deletes the specified directory, also deletes symbolic links

        path (string): The absolute/relative path of the directory we want to delete i.e. "/usr/bin/test"
        """

        if Local.dir_exists(path):
            shutil.rmtree(path)

    @staticmethod
    def list_directory(path):
        """ Returns the contents of a directory as two lists containing the files and sub-directories (this ignores links)

        path (string): The absolute/relative path of the directory we want to search i.e. "/usr/bin/test"
        """

        files = list()
        dirs = list()

        for item in os.listdir(path):
            item_path = '/'.join([path, item])

            if Local.dir_exists(item_path):
                dirs.append(item_path)

            elif Local.file_exists(item_path):
                files.append(item_path)

        return dirs, files
