""" Module parses a python file """

import ast
import logging
import re

log = logging.getLogger()

class PythonFileParser:
    """

    """

    def __init__(self):
        """

        """

        self.all_modules = dict()
        self.all_imports = dict()


    def parse(self, python_files):
        """

        """

        for module in python_files:

            log.debug("PARSING MODULE: %s", module)

            with open(module, 'r') as src:
                root = ast.parse(src.read())

            analyzer = Analyzer(python_files)
            analyzer.visit(root)
            imports = analyzer.get_imports()

            self.all_imports[module] = imports

        self.all_modules = self._create_module_list()

        return self.all_modules, self.all_imports

    ###############################
    # PRIVATE METHODS
    ###############################

    def _create_module_list(self):
        """

        """

        all_modules = dict()

        for import_list in self.all_imports.values():
            for import_obj in import_list:
                all_modules[import_obj.import_path] = import_obj.import_package

        return all_modules


class Import():
    """ Simple structure for holding module imports

    """

    def __init__(self, name, alias=None, path=None, package=None):
        """ initalises the datatypes for the Import structure

        import <name> as <alias>
        from <package> import <name> as <alias>
        """

        self.import_name = name
        self.import_alias = alias
        self.import_path = path
        self.import_package = package

    def __repr__(self):
        """ String representation of the object """
        return "from %s import %s local_module=[%s])" % (self.import_path, self.import_name, self.import_package)


class Analyzer(ast.NodeVisitor):
    """ Parses the information in the AST

    """

    def __init__(self, package_files):
        """ imports: Stores all imports in the AST, what's imported, where from and any alias it has """

        self.imports = list()
        self.package_files = package_files

    def visit_Import(self, node):
        """ Method called for all Import nodes in the AST graph """

        for alias in node.names:

            import_path = alias.name.replace('.', '/') + '.py'
            import_path, package = self._check_import_in_package(import_path)

            self.imports.append(Import(name=alias.name, alias=alias.asname, path=import_path, package=package))

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """ Method called for all ImportFrom nodes in the AST graph """

        for alias in node.names:

            # FIXME: If a relative import is used then node.module will be None, Will need to find a workaround for this
            if node.module:

                import_path = node.module.replace('.', '/') + '.py'
                import_path, package = self._check_import_in_package(import_path)

                self.imports.append(Import(name=alias.name, alias=alias.asname, path=import_path, package=package))

        self.generic_visit(node)

    def report(self):
        """ Prints the results of the analyzer to standard output, used for debugging """

        for imp in self.imports:
            print(imp)

    def get_imports(self):
        """ Returns all the imports in the AST for the python file """

        return self.imports

    ###############################
    # PRIVATE METHODS
    ###############################

    def _check_import_in_package(self, import_path):
        """
        Checks if the provided import path matches one of the package files
        Otherwise returns false to indicate the dependency is not part

        import_path (string): The path a module/package/class/function/expression is imported from
        """

        for file_path in self.package_files:
            if re.match('.*' + import_path + '$', file_path):
                return file_path, 'package'

        return import_path, 'standard'
