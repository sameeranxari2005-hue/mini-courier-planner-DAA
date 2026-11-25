import os
import random
import time
import matplotlib.pyplot as plt

from sorting import merge_sort_parcels
from knapsack import solve_knapsack_dp
from graph_routing import all_pairs_shortest_distances, nearest_neighbor_tsp


def generate_synthetic_case(num_parcels, num_locations, seed=42):
    rng = random.Random(seed + num_parcels)
    nodes = ["Depot"] + [f"L{i}" for i in range(1, num_locations)]
    graph = {u: {} for u in nodes}

    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if i != j and rng.random() < 0.55:
                w = rng.randint(2, 20)
                graph[u][v] = w
                graph[v][u] = w

    # Ensure Depot connects to all locations so graph stays connected
    for loc in nodes[1:]:
        if not graph[loc]:
            w = rng.randint(3, 15)
            graph["Depot"][loc] = w
            graph[loc]["Depot"] = w

    parcels = []
    for k in range(num_parcels):
        parcels.append(
            {
                "id": f"P{k + 1}",
                "weight": rng.randint(1, 10),
                "value": rng.randint(10, 100),
                "priority": rng.randint(1, 5),
                "deadline": rng.randint(1, 20),
                "destination": rng.choice(nodes[1:]),
            }
        )

    capacity = max(10, num_parcels * 3)
    return parcels, graph, capacity


def benchmark_sizes(sizes=(10, 25, 50, 100, 150)):
    results = []

    for n in sizes:
        parcels, graph, capacity = generate_synthetic_case(n, num_locations=min(25, n + 2))

        t0 = time.perf_counter()
        sorted_p = merge_sort_parcels(parcels)
        t1 = time.perf_counter()

        pack = solve_knapsack_dp(sorted_p, capacity)
        t2 = time.perf_counter()

        dist_matrix, _ = all_pairs_shortest_distances(graph)
        stops = [p["destination"] for p in pack["selected_parcels"]]
        nearest_neighbor_tsp(dist_matrix, stops, depot="Depot")
        t3 = time.perf_counter()

        results.append(
            {
                "n": n,
                "sort_ms": (t1 - t0) * 1000,
                "knapsack_ms": (t2 - t1) * 1000,
                "routing_ms": (t3 - t2) * 1000,
                "total_ms": (t3 - t0) * 1000,
            }
        )

    return results


def plot_results(results, out_path="outputs/runtime_chart.png"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    sizes = [r["n"] for r in results]

    plt.figure(figsize=(8, 5))
    plt.plot(sizes, [r["sort_ms"] for r in results], marker="o", label="Merge Sort")
    plt.plot(sizes, [r["knapsack_ms"] for r in results], marker="s", label="0/1 Knapsack DP")
    plt.plot(sizes, [r["routing_ms"] for r in results], marker="^", label="Dijkstra + NN TSP")
    plt.plot(sizes, [r["total_ms"] for r in results], marker="d", linestyle="--", label="Total Pipeline")

    plt.title("Mini-Courier Planner Runtime vs. Parcel Count")
    plt.xlabel("Number of Parcels (n)")
    plt.ylabel("Execution Time (ms)")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()


if __name__ == "__main__":
    data = benchmark_sizes()
    print(f"{'Parcels':>8} | {'Sort (ms)':>10} | {'Knapsack (ms)':>13} | {'Routing (ms)':>12} | {'Total (ms)':>10}")
    print("-" * 68)
    for row in data:
        print(
            f"{row['n']:>8} | {row['sort_ms']:>10.3f} | {row['knapsack_ms']:>13.3f} | "
            f"{row['routing_ms']:>12.3f} | {row['total_ms']:>10.3f}"
        )
    plot_results(data)
    print("\nSaved runtime chart to outputs/runtime_chart.png")