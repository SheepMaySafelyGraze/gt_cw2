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

edge_labels = {("H", "Ko0"):"5", ("H", "Ki0"): "4", ("H", "P0"): "4", ("H", "L0"): "5",
               ("L", "Ko0"):"2", ("L", "Ki0"): "3", ("L", "P0"): "3", ("L", "L0"): "1",
               ('P0', 'P1'): "x", ('P1', 'LS'): "3", ('P1', 'JCR'): "1", ('P1', 'HS'): "4", 
               ('Ko0', 'Ko1'): "3x", ('Ki0', 'Ki1'): "1.5x", ('L0', 'L1'): "2.5x", ('Ko1', 'LS'): "2", 
               ('Ko1', 'JCR'): "1", ('Ko1', 'HS'): "5", ('Ki1', 'LS'): "3", ('Ki1', 'JCR'): "1", 
               ('Ki1', 'HS'): "4", ('L1', 'LS'): "1", ('L1', 'JCR'): "2", ('L1', 'HS'): "5"}

nx.draw(G, pos=pos, node_color="#86AC99", node_size=1000, arrows=True)
nx.draw_networkx_labels(G, pos=pos)
nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_color='#86AC99'
)
plt.show()