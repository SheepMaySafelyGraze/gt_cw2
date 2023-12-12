import itertools
import numpy as np
import networkx as nx
import time
import matplotlib.pyplot as plt

G = nx.DiGraph()
nodes = ["H", "L", "P0", "P1", "LS", "JCR", "HS", "Ko0", "Ki0", "L0", "P1", "Ko1", \
         "Ki1", "L1"]
G.add_nodes_from(nodes)

edges1 = list(itertools.product(["H", "L"], ["Ko0", "Ki0", "P0", "L0"]))
edges2 = [(n1, n2) for n1, n2 in zip(["Ko0", "Ki0", "P0", "L0"], ["Ko1", "Ki1", "P1", "L1"])]
edges3 = list(itertools.product(["Ko1", "Ki1", "P1", "L1"], ["LS", "JCR", "HS"]))
edges = edges1 + edges2 + edges3
G.add_edges_from(edges)


def compute_costs(routes, edge_costs, G):
    """
    given a set of routes and costs, computes payoffs for each players
    :param routes: routes given as tuples of nodes, assume list of n tuples
    :param costs: costs for each edge, given as a dictionary of edges and cost functions
    :param G: networkx graph object giving underlying graph
    :return: payoffs for each of the n players
    """

    n = len(routes)  # number of players
    edges = G.edges

    edge_loads = {e: 0 for e in edges}
    costs = [0 for _ in range(n)]

    # computing edge loads
    for route in routes:
        for k in route:
            edge_loads[k] += 1

    # computing costs for each player
    for i, route in enumerate(routes):
        for edge in route:
            cost = edge_costs[edge]
            try:
                costs[i] += cost
            except TypeError:  # if cost is function of loads, evaluate
                costs[i] += cost(edge_loads[edge])

    return costs


# forming random, valid routes for testing
routes = []
N = 2
for i in range(N):
    route = [(edges1[np.random.choice(range(len(edges1)))])]
    route.append((route[0][1], route[0][1].replace("0", "1")))
    edges_final = [e for e in edges3 if e[0] == route[0][1].replace("0", "1")]
    route.append(edges_final[np.random.choice(range(len(edges_final)))])
    routes.append(route)

costs1 = {('H', 'P0'): 4,
          ('H', 'Ki0'): 4,
          ('H', 'Ko0'): 5,
          ('H', 'L0'): 5,
          ('L', 'P0'): 3,
          ('L', 'Ki0'): 3,
          ('L', 'Ko0'): 2,
          ('L', 'L0'): 1}


def get_wait_cost(serv_constant):
    # computes wait times given a serving speed constant
    return lambda x: serv_constant * x


serving_times = [1, 1.5, 3, 2.5]
outlets = ['P', 'Ki', 'Ko', 'L']
costs2 = {(o + '0', o + '1'): get_wait_cost(s) for o, s in zip(outlets, serving_times)}

costs3 = {('P1', 'LS'): 3,
          ('P1', 'JCR'): 1,
          ('P1', 'HS'): 4,
          ('Ki1', 'LS'): 3,
          ('Ki1', 'JCR'): 1,
          ('Ki1', 'HS'): 4,
          ('Ko1', 'LS'): 2,
          ('Ko1', 'JCR'): 1,
          ('Ko1', 'HS'): 5,
          ('Ko1', 'LS'): 2,
          ('Ko1', 'JCR'): 1,
          ('Ko1', 'HS'): 5,
          ('L1', 'LS'): 1,
          ('L1', 'JCR'): 2,
          ('L1', 'HS'): 5}

costs = costs1
costs.update(costs2)
costs.update(costs3)

print(routes)
compute_costs(routes, costs, G)

# iterating across all routes and thus computing social optimum

# forming iterator across all routes
H_edges = [e for e in edges1 if e[0] == 'H']
L_edges = [e for e in edges1 if e[0] == 'L']

H_routes = [e for e in itertools.product(H_edges, edges3) if e[0][1] == e[1][0].replace("1", "0")]
L_routes = [e for e in itertools.product(L_edges, edges3) if e[0][1] == e[1][0].replace("1", "0")]

sum = 0
min_costs = np.inf  # keeping count of minimum cost obtained
social_optimum_route = None
social_optimum_routes = []
cost_list = []
start = time.time()
for play in itertools.product(itertools.combinations_with_replacement(H_routes, 5),
                              itertools.combinations_with_replacement(L_routes, 5)):
    sum += 1
    routes = []
    for routes_i in play:  # obtaining all routes by adding 'implicit' waiting transitions
        for r in routes_i:
            path = [r[0], (r[0][1], r[1][0]), r[1]]
            routes.append(path)

    route_costs = compute_costs(routes, edge_costs=costs, G=G)
    avg_cost = np.mean(route_costs)
    cost_list.append(avg_cost)
    if avg_cost < min_costs:
        min_costs = avg_cost
        social_optimum_route = routes
    if avg_cost == 8.25:  # known social optimum
        social_optimum_routes.append(routes)


    if sum % 1000000 == 0:
        print(f'{100*sum/19e6} took {time.time() - start:.2f}')


for i in social_optimum_routes:
    print(i)


