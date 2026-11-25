# Mini-Courier Planner (DAA Capstone Assignment)

**Student Name:** Sameer Ansari
**Roll No.:** 2501010107  
**Section:** A  

An integrated Python application for **Design & Analysis of Algorithms (ETCCDA302)** that prioritizes parcels, selects an optimal load for a delivery box/van, computes shortest paths across a delivery network, generates an ordered delivery route, and benchmarks runtime performance across dataset sizes.

## 1. Problem Design & Architecture
- **Parcel Attributes:** `id`, `weight` (integer), `value` (priority/revenue score), `priority`, `deadline`, and `destination`.
- **Delivery Graph:** Weighted adjacency dictionary (`graph[u][v] = distance`) connecting `"Depot"` and delivery locations.
- **Pipeline Flow:**
  1. **Prioritization (Merge Sort):** Orders parcels by highest `priority` first, then earliest `deadline`.
  2. **Package Selection (0/1 Knapsack DP):** Finds the highest-value parcel subset fitting within box weight `capacity` for one trip and backtracks to list selected parcels.
  3. **Shortest Paths & Routing (Dijkstra + Nearest-Neighbor TSP):** Computes shortest paths between stops using a min-heap (`heapq`) and builds a tour starting and ending at `"Depot"` by repeatedly visiting the nearest unvisited stop.
  4. **Benchmarking & Visualization:** Runs multiple dataset sizes (`n = 10, 25, 50, 100, 150`) and plots execution times to `outputs/runtime_chart.png`.

## 2. Complexity Summary
- **Merge Sort:** Time $O(n \log n)$, Space $O(n)$
- **0/1 Knapsack (2D DP):** Time $O(n \cdot W)$, Space $O(n \cdot W)$, where $W$ is capacity
- **Dijkstra (Min-Heap):** Time $O((V + E) \log V)$, Space $O(V)$
- **Nearest-Neighbor TSP:** Time $O(k^2)$, Space $O(k)$, where $k$ is the number of stops

## 3. Future Optimizations
- **Knapsack Space:** Reduce space from $O(n \cdot W)$ to $O(W)$ using a 1D array (paired with item tracking if full subset recovery is required).
- **TSP Quality:** Nearest-Neighbor is a fast approximation and is not guaranteed optimal; applying **2-opt** local search can shorten routes further.

## 4. How to Run
```bash
pip install matplotlib
python main.py
python benchmark.py