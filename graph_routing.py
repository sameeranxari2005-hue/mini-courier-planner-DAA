import heapq


def dijkstra_shortest_path(graph, start):
    """
    Computes shortest path distances and parent pointers from `start`
    to all reachable nodes in a weighted graph using a min-heap.
    Time Complexity: O((V + E) log V) | Space Complexity: O(V)
    """
    distances = {node: float("inf") for node in graph}
    parent = {node: None for node in graph}
    distances[start] = 0
    pq = [(0, start)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        if curr_dist > distances[curr_node]:
            continue

        for neighbor, weight in graph[curr_node].items():
            new_dist = curr_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                parent[neighbor] = curr_node
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, parent


def reconstruct_path(parent, start, target):
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        if curr == start:
            break
        curr = parent[curr]
    path.reverse()
    return path if path and path[0] == start else []


def all_pairs_shortest_distances(graph):
    dist_matrix = {}
    parent_map = {}
    for node in graph:
        dists, parents = dijkstra_shortest_path(graph, node)
        dist_matrix[node] = dists
        parent_map[node] = parents
    return dist_matrix, parent_map


def nearest_neighbor_tsp(dist_matrix, stops, depot="Depot"):
    """
    Approximates a delivery route starting at `depot`, visiting all unique
    `stops` using the closest unvisited stop next, and returning to `depot`.
    Time Complexity: O(k^2) where k is the number of stops | Space Complexity: O(k)
    """
    unvisited = [s for s in dict.fromkeys(stops) if s != depot]
    route = [depot]
    total_distance = 0.0
    current = depot

    while unvisited:
        next_stop = min(unvisited, key=lambda s: dist_matrix[current][s])
        leg_dist = dist_matrix[current][next_stop]
        if leg_dist == float("inf"):
            raise ValueError(f"No path from {current} to {next_stop}")
        total_distance += leg_dist
        route.append(next_stop)
        unvisited.remove(next_stop)
        current = next_stop

    return_leg = dist_matrix[current][depot]
    if return_leg == float("inf"):
        raise ValueError(f"No return path from {current} to {depot}")
    total_distance += return_leg
    route.append(depot)

    return route, total_distance