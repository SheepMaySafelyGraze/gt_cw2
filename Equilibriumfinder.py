# function to perform iterative search and find equilibrium

import itertools
import numpy as np
import networkx as nx
import time
import matplotlib.pyplot as plt

# Setup and defining network

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


# all routes from each possible start point
H_edges = [e for e in edges1 if e[0] == 'H']
L_edges = [e for e in edges1 if e[0] == 'L']

H_routes = [e for e in itertools.product(H_edges, edges3) if e[0][1] == e[1][0].replace("1", "0")]
L_routes = [e for e in itertools.product(L_edges, edges3) if e[0][1] == e[1][0].replace("1", "0")]


def check_is_max(routes, player_costs, player_ind, edge_costs, G,
                 return_routes=False, debug=False):
    # given a set of routes, check if player_ind's position is maximising given other routes

    player_route = routes[player_ind]
    cost_i = player_costs[player_ind]

    try:  # get alternative routes starting at the same spot
        alternatives = eval(player_route[0][0] + '_routes')
        assert type(alternatives) == list
    except Exception as _:
        print(f"failed to parse first position! {player_route[0][0]}")

    routes_alt = routes.copy()
    for alt in alternatives:
        routes_alt[player_ind] = alt
        alt_costs = compute_costs(routes_alt, edge_costs=costs, G=G)
        alt_cost_i = alt_costs[player_ind]
        if alt_cost_i < cost_i:  # if better route found
            if debug:
                print(f"Better route found for {player_ind}, cost improvement = {cost_i - alt_cost_i}")
            if return_routes:
                return alt_costs, routes_alt, True
            return alt_costs
        if debug:
            print("No better route found!")
    if return_routes:
        return player_costs, routes, False
    return player_costs

# fixing H_routes and L_routes by adding intermediate wait edges
H_routes = [tuple([r[0], (r[0][1], r[1][0]), r[1]]) for r in H_routes]
L_routes = [tuple([r[0], (r[0][1], r[1][0]), r[1]]) for r in L_routes]


# function to form random valid routes

def get_random_routes(N, start=None):
    # returns random routes for N players, with fixed start location
    # if start is None, chooses a random start location
    routes = []

    for i in range(N):
        if start is None:
            route = [(edges1[np.random.choice(range(len(edges1)))])]
        else:
            start_edges = eval(start + '_edges')
            route = [(start_edges[np.random.choice(range(len(start_edges)))])]
        route.append((route[0][1], route[0][1].replace("0", "1")))
        edges_final = [e for e in edges3 if e[0] == route[0][1].replace("0", "1")]
        route.append(edges_final[np.random.choice(range(len(edges_final)))])
        routes.append(tuple(route))

    return routes


def iterative_search(routes_init=None, N=None, maxit=1000,
                     return_costs=False, debug=False):
    # iteratively improves players routes, hoping to converge on an equilibrium
    # if no routes_init provided, generates random initial routes with N players
    # if found equilibrium, returns along with achieved costs
    # it is likely this procedure gets stuck in a loop - beware!
    equib_found = False
    it = 0
    cost_list = []  # to store costs allowing visualisation of improvement

    if routes_init is None:
        try:
            routes_init = get_random_routes(N // 2, 'H') + get_random_routes(N - N // 2, 'L')
        except TypeError:
            print("please specify either number of players or initial routes")
            return

    routes = routes_init
    players_costs = compute_costs(routes, edge_costs=costs, G=G)

    while it < maxit and equib_found == False:
        equib_found = True
        for player_ind in range(N):
            players_costs, routes, improved = check_is_max(routes, players_costs,
                                                           player_ind, edge_costs=costs,
                                                           G=G, return_routes=True, debug=debug)
            equib_found = equib_found and not improved
        cost_list.append(players_costs)
        it += 1

    if equib_found == True:
        if debug:
            print(f"Equilibrium found after {it} iterations")
        if return_costs:
            return routes, cost_list
        return routes

    if debug:
        print(f"No equilibrium found after {it} iterations. Terminating...")
    return


routes, cost_list = iterative_search(N=10, maxit=500, return_costs=True,
                                     debug=False)

for i in range(len(routes)):
    # plt.plot([l[i] for l in cost_list], alpha = 0.05)
    pass
plt.plot([np.mean(l) for l in cost_list], label="average cost")
plt.legend()
plt.show()

print(f"One equilibrium is: \n {routes}")







