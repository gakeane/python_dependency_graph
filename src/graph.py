
"""
This module creates graphs using GraphViz.
It should be general purpose so it can be reused in other projects

"""

import logging

from graphviz import Digraph

log = logging.getLogger()


NODE_COLORS = {'package': 'red',
               'standard': 'blue'}

class Graph():
    """ Class for creating graps using graphViz

    """

    def __init__(self, graph_format='png'):
        """ Initialise the type of graph to be built

        graph_format (string): The file format of the graph visualisation [png, pdf]
        """

        self.graph = Digraph("Dependencies", format=graph_format, filename='dependency_graph.gv', node_attr={'color': 'lightblue2', 'style': 'filled'})
        self.graph.attr(size='8000,8000')

    # FIXME: change this to work with lists of Node and Edge objects
    def build_graph(self, nodes, edges):
        """ Create a graph from a list of nodes and edges

        nodes (list): Ideally this is a list of Node objects, however currently implemented as a dictionary
        edges (list): Ideally this is a list of Edge objects, however currently implemented as a list of dictionaries
        """

        log.info("Building Graph with [%s] nodes and [%s] edges" % ('NOT_IMPLEMENTED', 'NOT_IMPLEMENTED'))

        for node, node_type in nodes.items():
            self.graph.node(node, node.replace('tmp_git_repo/', '', 1), color=NODE_COLORS[node_type])

        for left_edge, right_edges in edges.items():
            for right_edge in right_edges:
                self.graph.edge(left_edge, right_edge.import_path, label=right_edge.import_name)

    def render_graph(self, view=True):
        """ Render the graph after it has been created

        view (boolean): When True displays the dependency graph once it's created
        """

        log.debug("Rendering Graph to image file [%s]" % 'NOT_IMPLEMENTED')

        if view:
            self.graph.view()
        else:
            self.graph.render()
