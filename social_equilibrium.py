import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
nodes = ["H", "L", "P0", "P1", "LS", "JCR", "HS", "Ko0", "Ki0", "L0", "P1", "Ko1", \
         "Ki1", "L1"]
G.add_nodes_from(nodes)

edges1 = list(itertools.product(["H", "L"], ["Ko0", "Ki0", "P0", "L0"]))
edges2 = [(n1, n2) for n1, n2 in zip(["Ko0", "Ki0", "P0", "L0"], ["Ko1", "Ki1", "P1", "L1"])]
edges3 = list(itertools.product(["Ko1", "Ki1", "P1", "L1"], ["LS", "JCR", "HS"]))
edges = edges1 + edges2 + edges3
G.add_edges_from(edges)
print(G.edges)
pos = nx.spring_layout(G)
nx.draw(G, pos=pos, "cyan")
nx.draw_networkx_labels(G, pos=pos)
plt.show()

def compute_costs(routes, edge_costs, nodes, edges):
    """
    given a set of routes and costs, computes payoffs for each players
    :param routes: routes given as tuples of nodes, assume list of n tuples
    :param costs: costs for each node, given as a dictionary of edges and cost functions
    :return: payoffs for each of the n players
    """

    n = len(routes)  # number of players
    costs = [0 for i in range(n)]

    for i, route in enumerate(routes):
        for k in route[:-1]:
            pass


