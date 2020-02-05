## Table of Contents
1. [Overview](#Overview)
2. [Usage](#Usage)
3. [Dependencies](#Dependencies)
4. [Assumptions](#Assumptions)
5. [Design](#Design)
6. [Known Issues](#Known-Issues)
7. [Futher Work](#Futher-Work)

## Overview
The Python Dependency Graphing Tool (PDGT) creates a visual representation of the dependencies between python modules. The tool can be pointed to a local directory or provided with the URL of a Git repository. PDGT locates all python modules within the provided directory and parses them using an AST (abstract-syntax tree). The AST of each file is traversed to identify imports and dependencies. Finally the [GraphViz](https://www.graphviz.org/) library is used to create a dependency graph in the DOT language which can be rendered to several different formats.

## Usage
<pre>
usage: main.py [-h] [-r REPOSITORY] [-d DIRECTORY] [-i IGNORE_FILES]
               [-f {png,pdf}] [-v] [-c] [-s] [-vi]

optional arguments:
  -h, --help            show this help message and exit
  -r REPOSITORY, --repository REPOSITORY
                        URL to python git repository to be evaluated
  -d DIRECTORY, --directory DIRECTORY
                        Path to local python directory to be evaluated
  -i IGNORE_FILES, --ignore-files IGNORE_FILES
                        Path to file containing list of ignore
                        files/directories
  -f {png,pdf}, --format {png,pdf}
                        The file type for dependency graph [png, pdf]
  -v, --verbose         increase output verbosity
  -c, --clean           If set won't clean temporary files or directories the
                        tool creates
  -s, --shell           Git commands run from the default shell, (not
                        recommended)
  -vi, --view           If set the dependecy graph will be rendered but not
                        displayed

</pre>

### Notes

- The __-r__ option will cause the tool to clone the specified Git repository to the local host. This will be stored in a temporary directory /tmp_repo which will be cleaned up once the tool completes.
  - _This has not yet been tested using SSL certs_.

- The __-d__ argument specifies where the tool should start scanning from. Normally this would be the root of the project however a sub-directory can also be specified. In this case only modules in this sub-directory will be parsed. If not specified this will default to /tmp_repo
  - _Specifying a sub-directory for a git repository is currently not functioning_.

- The __-i__ argument can be used to pass a list of files or directories which should be ignored.
  - _This is still under development and is not currently operational_.


### Examples
<pre># python3 main.py -r https://github.com/gakeane/python_dependency_graph -d python_dependency_graph </pre>
<pre># python3 main.py -d python_dependency_graph/src -v</pre>

## Dependencies
The PDGT tool has the following dependencies

### Git
It is required to have the Git CLI tool installed for the tool to clone into git repositories. Git can be installed on Windows with the [Git For Windows](https://gitforwindows.org/) executable. See the known issues section for more information about running the tool on Windows.

On Redhat, Centos, Fedora
<pre>sudo yum update && sudo yum install git</pre>

On Debian, Ubuntu
<pre>sudo apt update && sudo apt install git</pre>

### GraphViz
Both the GraphViz library and the python plugin are required by PDGT.

On Redhat, Centos, Fedora
<pre>
sudo yum-config-manager --add-repo graphviz-rhel.repo
sudo yum-config-manager --add-repo graphviz-rhel.repo
sudo yum install graphviz

sudo pip3 install pydot graphviz
</pre>

On Debian, Ubuntu
<pre>
sudo apt install graphviz

sudo pip3 install pydot graphviz
</pre>

## Assumptions

 - Relative imports are ignored in the current version of PDGT. It was difficult to determine the owner module for relative imports. The tool will only consider absolute imports. The additon of relative imports can be included in a later version.
 - The current implementation of the tool does not detect specific calls of an imported module, only the import. Reliably extracting this information from the AST required a large amount of logic that I could not implement within the time constraints. Most function/method calls are contained in a _Name_ Node within the AST. This however would not identify all imports. The use of expressions and inheriting from an imported class would be missed. Due to the large variety of the python programming language this feature has not been implemented. Missing this feature may not be a bad thing as additonal edges for every method call will over-crowd the dependency graph in large projects. A more interactive graph viewer would likely be required.

## Design
Operation of the PDGT tool consists of one optional stage and three mandatory stages.
- The optional stage clones a git repository into onto the local machine. This is done by starting a subprocess which runs the _git clone_ operation. Instead of cloning a Git repository PDGT can be pointed to a local directory. Ensure you have read permissions for this directory.
- The first mandatory stage recursively moves through the target directory and identifies all python modules while ignoring other file types. An additional feature in developement will allow the user to specify a list of files or directories to be ignored.
- The second mandatory stage creates an asymmetric syntax tree (AST) of each python module. The tree is traversed and all Import nodes are visited to identify a list of dependencies for each module. It was decided not to load the python modules to identify imports as this could result in unwanted code being executed on the client machine. An AST tree was used to parse the python code as it proved to be faster and more reliable than line by line parsing.
- Finally GraphViz is used to create a graph where each module is a node and each dependency is an edge. The resulting graph is rendered to either a png or a pdf. Additonal formats will be added at a later point.

### local

- _class_ __Local__: Static class containing methods for executing commands and managing directories on the local machine.

### logger

- _function_ __setup_logs__: Creates log handlers and formatters so that the root log will display to a file called Parser.log and to the console. The _verbose_ argument can be set to True to display Debug message to the console.

### data

- _function_ __parse_user_input__: Parses the arguments passed to PDGT from the command line.

### load

- _class_ __GitHub__: Class for executing Git commands on the local machine. This was implemented instead of using GitPython to reduce the number of dependencies. This may be replaced with GitPython in a later version once a Docker file has been created.

  - _class_ __GitHub__ _method_ __clone__: Clones a repository to the local machine.

- _class_ __DirectoryParser__: Class for moving through a directory and identifying all python modules

  - _class_ __DirectoryParser__ _method_ __get_python_files__: Returns a list of all python files in a directory

### parse
This section of the code base requires some refactoring. It is suggested to create Node and Edge classes for tracking modules and dependencies. Each module is a Node and each dependency is an Edge.

- _class_ __PythonFileParser__: Class used to identify all imports in a list of python modules.

  - _method_ __parse__: Creates an AST of each python module and uses this to identify all imports.

- _class_ __Import__: Structure like class used to store data about each import. This will likely be replaced by Edge and Node classes

- _class_ __Analyzer__: Child class of NodeVisitor, vists all nodes on an AST.

  - _method_ __visit_Import__: Called for all import declarations.

  - _method_ __visit_ImportFrom__: Called for all from <path> import <item> declarations.
### graph

- _class_ __Graph__: Class which handles the creation and rendering of VizGraph DiGraph

  - _method_ __build_graph__: Given a list of nodes and edges, builds the graph object

  - _method_ __render_graph__: Renders a Graph to a png or pdf, ensure the graph has been built first with Graph().build_graph


## Testing
PDGT has been tested on red hat 7 (linux) and windows 10. See [known issues](#Known-Issues) for details about running the tool on Windows. Additionally there are several unit tests in the tests sub-folder. These tests confirm basic operation of cloning form a git repository, identifying all python files in a directory and identifying all imports in a list of python modules. The test suite is based of the python unittest module and can be run with the following command.

<pre>python3 test.py</pre>

## Known Issues

### PDGT and Git on Windows
PDGT uses the python subprocess Popen module to make system calls. On windows Popen starts a sub-processes by calling the executable for a program (.exe). When installed on Windows Git does not have an explict .exe executable so cannot be called this way. The tool will therefore return a FileNotFoundError. The work around is to start a system shell and call the Git command in this shell. By default enabling execution in the shell is disabled as it presents a security risk. When passed the __-s__ argument PDGT will execute any git commands in the default shell on the your windows system. When using this option ensure that there is nothing undue about the git repository your cloning.

### Repo CleanUp on Windows
The shutil rmtree method used to delete repositories fails on Windows due to a permission issue. This means temporary repositories in /tmp_repo will not be removed when PDGT completes. The workaround is to used to __-c__ argument to prevent automatic cleanup and then to manually delete /tmp_repo

### Search Repository Sub-directory
Using the __-r__ and __-d__ arguments to specify both a git repository to be cloned and a sub-directory is currently prevented due to a minor bug. This will be fixed soon. The work around is to manually clone the repository and then run PDGT with the desired sub-directory

## Further Work

### Graph visualisation Improvements
I was not famillar with the GraphViz Library when developing PDGT. There are likely many imporvements that can be made with regards to the visual design of the Graph. This would include the size of the graph, the shape and colour of Nodes and how edges are labelled.

### Performance Improvements
PDGT has been tested on [packages](https://github.com/sqlmapproject/sqlmap) containing roughly 1000 files and 500 python modules. The performance bottleneck occurs when rendering the VizGraph. This may be improved by rendering to several smaller classes. Additional performance could also be gained at the file parsing stage through the use of some clever refactoring, this would only be noticible for very large packages.

### Ignore standard Library imports
Allow the user to pass an argument which will tell PDGT to ignore all imports and modules relating to python standard library modules. This can be extended to also ignore third party modules which are not part of the package.

### Additional Parsing of the AST for dependency calls
As mentioned in the [Assumptions](#Assumptions) section additional parsing of the AST is required to detect any usage or calls made by an imported module.

### Additional Testing
Code was primarily tested on a linux machine against a small number of repositories. Additional testing is required to ensure robust operation. We should also expand the unit tests to cover a greater range of functionality.

### Code Cleanup
Code was implemented quickly such that some modules, classes and methods/functions having incomplete or missing doc-strings. A review of what the tool is logging. Renaming of some variables, including the module names such that they more clearly convey their purpose.

### Docker integration
Write a docker file for PDGT on a linux host with the dependencies already installed.
