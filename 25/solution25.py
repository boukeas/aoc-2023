from collections import Counter, defaultdict, deque
from random import choice
from sys import argv

from tools25 import pairwise


def edge_from_nodes(node_1, node_2):
    """
    Return an edge, i.e. a *sorted* pair of nodes

    The nodes in an edge are sorted alphabetically so that
    edges are unique even though they are undirected.
    """
    return tuple(sorted((node_1, node_2)))


def parse_file(lines):
    """
    Generate all graph edges from the input file
    """
    for line in lines:
        left_node, right_nodes = line.strip().split(": ")
        right_nodes = right_nodes.strip().split()
        for right_node in right_nodes:
            yield edge_from_nodes(left_node, right_node)


def get_graph(edges):
    """
    Return a graph from an iterable of edges

    In this case, a graph is a dict mapping each node to
    a set of connected nodes
    """
    connections = defaultdict(set)
    for left_node, right_node in edges:
        connections[left_node].add(right_node)
        connections[right_node].add(left_node)
    return connections


def shortest_paths(start_node, graph):
    """
    Given a start node in a graph, perform a depth-first seach
    to create and return a dict that maps each node that is
    reachable from the start node to the shortest path from
    the start node. A path is a tuple of nodes.
    """
    # the frontier of unexplored nodes
    queue = deque([start_node])
    # the current result: a dict mapping each node that has been
    # visited so far to a path from the start node
    connected = {start_node: (start_node,)}
    while len(queue) > 0:
        node = queue.popleft()
        new_nodes = graph[node].difference(connected)
        queue.extend(new_nodes)
        path = connected[node]
        connected.update(
            {
                new_node: path + (new_node,)
                for new_node in new_nodes
            }
        )
    return connected


if __name__ == '__main__':
    with open(argv[1]) as file:
        graph = get_graph(parse_file(file.readlines()))

    # number of random starting nodes
    try:
        nb_floods = int(argv[2])
    except IndexError:
        nb_floods = 20

    nodes = list(graph)
    # count how many times an edge is visited
    counters = Counter()
    for i in range(nb_floods):
        # pick a random node and compute a path to *each* other node
        node = choice(nodes)
        paths = shortest_paths(node, graph)
        # iterate over all edges in all the paths and
        # update the counters
        for path in paths.values():
            counters.update(
                edge_from_nodes(node1, node2)
                for node1, node2 in pairwise(path)
            )

    # remove the three most common edges from the graph
    for edge, _ in counters.most_common(3):
        node1, node2 = edge
        graph[node1].difference_update({node2})
        graph[node2].difference_update({node1})

    # perform another final "flood": if the graph has been
    # bisected then only a subset of the nodes should be
    # reachable and we can count how many these are
    group_size_1 = len(shortest_paths(node, graph))
    group_size_2 = len(nodes) - group_size_1
    print(group_size_1, group_size_2, group_size_1 * group_size_2)
