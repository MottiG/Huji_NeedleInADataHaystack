import networkx as nx

EGO_NET_PATH = 'fbegonet.txt'
K = 4  # size of cliques for clique_percolation


def get_graph(path: str) -> nx.Graph:
    """
    Get graph from a given path of a text file with each line represent single edge of the graph
    """
    with open(path, 'r') as f:
        list_of_edges = [line.strip().split() for line in f.readlines()]
        g = nx.Graph()
        g.add_edges_from(list_of_edges)
        return g


def clique_percolation(k: int, g: nx.Graph):
    """
    Get the communities of a given graph using clique percolation.
    this is brute-force function. if we add a dictionary that maps any node with its cliques, and then go only
    over cliques with at least one interaction, it could be more efficient
    :param k: number of node of each clique
    :param g: networkx graph
    :return: list of communities, sorted by size (increase order)
    """
    cliques = [frozenset(clq) for clq in nx.enumerate_all_cliques(g) if len(clq) == k]

    graph_of_cliques = nx.Graph()
    for clq in cliques:
        is_isolate = True  # this clique is not connected to any other clique
        for other_clq in cliques:
            if clq is other_clq:
                continue
            if len(clq.intersection(other_clq)) >= k-1 and not graph_of_cliques.has_edge(clq, other_clq):
                is_isolate = False
                graph_of_cliques.add_edge(clq, other_clq)
        if is_isolate:
            graph_of_cliques.add_node(clq)

    # create communities:
    communities = []
    for component in nx.connected_components(graph_of_cliques):
        communities.append(sorted(frozenset.union(*component)))

    return sorted(communities, key=len)

if __name__ == '__main__':

    graph = get_graph(EGO_NET_PATH)
    a_ans = '# of nodes: ' + str(graph.number_of_nodes()) + '\n'
    a_ans += '# of edges: ' + str(graph.number_of_edges())
    print('(a)\n' + a_ans)
    connected_components = sorted(nx.connected_components(graph), key=len, reverse=True)  # list of lists of connected nodes
    b_ans = '# of connected components: ' + str(len(connected_components)) + '\n'
    b_ans += '# of nodes in biggest component: ' + str(len(connected_components[0]))
    print('\n(b)\n' + b_ans)
    communities = clique_percolation(K, graph)
    c_ans = '# of communities: ' + str(len(communities)) + '\n'
    print('\n(c)\n' + c_ans + 'nodes of communities:')
    for community in communities:
        print(community)


