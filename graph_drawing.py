import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import itertools

G = nx.DiGraph()
nodes = ["H", "L", "P0", "P1", "LS", "JCR", "HS", "Ko0", "Ki0", "L0", "P1", "Ko1", \
         "Ki1", "L1"]
G.add_nodes_from(nodes)

edges1 = list(itertools.product(["H", "L"], ["Ko0", "Ki0", "P0", "L0"]))
edges2 = [(n1, n2) for n1, n2 in zip(["Ko0", "Ki0", "P0", "L0"], ["Ko1", "Ki1", "P1", "L1"])]
edges3 = list(itertools.product(["Ko1", "Ki1", "P1", "L1"], ["LS", "JCR", "HS"]))
edges = edges1 + edges2 + edges3
G.add_edges_from(edges)
print(G.edges)
pos = {}
pos["H"] = np.array([-9, 5])
pos["L"] = np.array([-9, -5])
pos["P0"] = np.array([-3, 15])
pos["Ki0"] = np.array([-3, 5])
pos["Ko0"] = np.array([-3, -5])
pos["L0"] = np.array([-3, -15])
pos["P1"] = np.array([3, 15])
pos["Ki1"] = np.array([3, 5])
pos["Ko1"] = np.array([3, -5])
pos["L1"] = np.array([3, -15])
pos["LS"] = np.array([9, 10])
pos["JCR"] = np.array([9, 0])
pos["HS"] = np.array([9, -10])
nx.draw(G, pos=pos, node_color="#86AC99", node_size=1000, arrows=True)
nx.draw_networkx_labels(G, pos=pos)
plt.show()