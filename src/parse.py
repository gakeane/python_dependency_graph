""" Module parses a python file """

import ast


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

        for file_id, python_file in enumerate(python_files):

            with open(python_file, 'r') as src:
                root = ast.parse(src.read())

            analyzer = Analyzer()
            analyzer.visit(root)

            imports = analyzer.get_imports()

            self.all_modules[python_file] = file_id
            self.all_imports[python_file] = imports


class Import():
    """ Simple structure for holding module imports

    """

    def __init__(self, name, alias=None, path=None):
        """ initalises the datatypes for the Import structure

        import <name> as <alias>
        from <path> import <name> as <alias>
        """

        self.import_name = name
        self.import_alias = alias
        self.import_path = path

    def __repr__(self):
        """ String representation of the object """
        return "from %s import %s as %s)" % (self.import_path, self.import_name, self.import_alias)


class Analyzer(ast.NodeVisitor):
    """ Parses the information in the AST

    """

    def __init__(self):
        """ imports: Stores all imports in the AST, what's imported, where from and any alias it has """

        self.imports = list()

    def visit_Import(self, node):
        """ Method called for all Import nodes in the AST graph """

        for alias in node.names:
            self.imports.append(Import(name=alias.name, alias=alias.asname))

        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """ Method called for all ImportFrom nodes in the AST graph """

        for alias in node.names:
            self.imports.append(Import(name=alias.name, alias=alias.asname, path=node.module))

        self.generic_visit(node)

    def report(self):
        """ Prints the results of the analyzer to standard output, used for debugging """

        for imp in self.imports:
            print(imp)

    def get_imports(self):
        """ Returns all the imports in the AST for the python file """

        return self.imports
