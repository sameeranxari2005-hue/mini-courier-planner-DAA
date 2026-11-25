from sorting import merge_sort_parcels
from knapsack import solve_knapsack_dp
from graph_routing import (
    all_pairs_shortest_distances,
    nearest_neighbor_tsp,
    reconstruct_path,
)


def build_sample_data():
    parcels = [
        {"id": "P1", "weight": 4, "value": 40, "priority": 2, "deadline": 5, "destination": "A"},
        {"id": "P2", "weight": 7, "value": 85, "priority": 3, "deadline": 2, "destination": "B"},
        {"id": "P3", "weight": 5, "value": 55, "priority": 1, "deadline": 4, "destination": "C"},
        {"id": "P4", "weight": 3, "value": 35, "priority": 3, "deadline": 3, "destination": "D"},
        {"id": "P5", "weight": 6, "value": 70, "priority": 2, "deadline": 1, "destination": "E"},
    ]

    graph = {
        "Depot": {"A": 4, "B": 8, "C": 6},
        "A": {"Depot": 4, "B": 5, "D": 7},
        "B": {"Depot": 8, "A": 5, "C": 3, "E": 6},
        "C": {"Depot": 6, "B": 3, "D": 4, "E": 9},
        "D": {"A": 7, "C": 4, "E": 2},
        "E": {"B": 6, "C": 9, "D": 2},
    }

    box_capacity = 14
    return parcels, graph, box_capacity


def run_planner(parcels, graph, capacity, show_dp=True):
    print("=== 1. SORTED PARCELS (Priority DESC, Deadline ASC) ===")
    sorted_parcels = merge_sort_parcels(parcels)
    for p in sorted_parcels:
        print(
            f"  {p['id']} | wt={p['weight']} | val={p['value']} | "
            f"prio={p['priority']} | due={p['deadline']} | dest={p['destination']}"
        )

    print("\n=== 2. 0/1 KNAPSACK PACKING PLAN ===")
    pack = solve_knapsack_dp(sorted_parcels, capacity)
    print(f"  Box Capacity     : {capacity}")
    print(f"  Total Weight Used: {pack['total_weight']} (Remaining: {pack['remaining_capacity']})")
    print(f"  Total Value      : {pack['total_value']}")
    print("  Selected Parcels :")
    for p in pack["selected_parcels"]:
        print(f"    - {p['id']} -> Destination {p['destination']} (wt={p['weight']}, val={p['value']})")

    if show_dp:
        print("\n  DP Table (rows=0..n parcels, cols=0..capacity):")
        for row in pack["dp_table"]:
            print("   ", row)

    print("\n=== 3. SHORTEST PATHS & ROUTE PLAN ===")
    dist_matrix, parent_map = all_pairs_shortest_distances(graph)
    stops = [p["destination"] for p in pack["selected_parcels"]]
    route, total_dist = nearest_neighbor_tsp(dist_matrix, stops, depot="Depot")

    print("  Ordered Delivery Route:", " -> ".join(route))
    print(f"  Total Route Distance  : {total_dist}")
    print("  Leg Breakdown:")
    for i in range(len(route) - 1):
        u, v = route[i], route[i + 1]
        leg_path = reconstruct_path(parent_map[u], u, v)
        print(f"    {u} -> {v}: dist={dist_matrix[u][v]}, path={' -> '.join(leg_path)}")


if __name__ == "__main__":
    parcels, graph, capacity = build_sample_data()
    run_planner(parcels, graph, capacity, show_dp=True)