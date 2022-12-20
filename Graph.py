def construct_graph(nodes, init_graph):
    graph = {}
    for node in nodes:
        graph[node] = {}

    graph.update(init_graph)

    for node, edges in graph.items():
        for adjacent_node, value in edges.items():
            if not graph[adjacent_node].get(node, False):
                graph[adjacent_node][node] = value

    return graph


class Graph(object):
    def __init__(self, nodes, init_graph):
        self.nodes = nodes
        self.graph = construct_graph(nodes, init_graph)

    def get_nodes(self):
        return self.nodes

    def get_outgoing_edges(self, node):
        connections = []
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False):
                connections.append(out_node)
        return connections

    def value(self, node1, node2):
        return self.graph[node1][node2]
    #
    # CALL
    # gds.graph.project(
    #     'myGraph',
    #     'Intersection',
    #     'route',
    #     {
    #         nodeProperties: ['latitude', 'longitude'],
    #         relationshipProperties: 'length'
    #     }
    # )

    # dbms.security.procedures.whitelist = algo. *, apoc. *
    # dbms.security.procedures.unrestricted = algo. *, apoc. *