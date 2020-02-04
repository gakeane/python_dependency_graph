
"""

"""

from graphviz import Digraph


NODE_COLORS = {'package': 'red',
               'standard': 'blue'}

class Graph():
    """

    """

    def __init__(self):
        """

        """

        self.graph = Digraph("Dependencies", format='png', filename='dependency_graph.gv', node_attr={'color': 'lightblue2', 'style': 'filled'})
        self.graph.attr(size='8000,8000')

    def build_graph(self, nodes, edges):
        """

        """

        for node, node_type in nodes.items():
            print(node, NODE_COLORS[node_type])
            self.graph.node(node, node.replace('tmp_git_repo/', '', 1), color=NODE_COLORS[node_type])

        for left_edge, right_edges in edges.items():
            for right_edge in right_edges:
                self.graph.edge(left_edge, right_edge.import_path)


    def render_graph(self):
        """

        """

        self.graph.view()
        # self.graph.render('dependency_graph', view=True)
