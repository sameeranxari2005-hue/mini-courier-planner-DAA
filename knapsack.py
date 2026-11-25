def solve_knapsack_dp(parcels, capacity):
    """
    Solves 0/1 Knapsack using a 2D DP table to maximize total value
    without exceeding `capacity` (integer weight).
    Time Complexity: O(n * capacity) | Space Complexity: O(n * capacity)
    """
    n = len(parcels)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        wt = parcels[i - 1]["weight"]
        val = parcels[i - 1]["value"]
        for w in range(capacity + 1):
            if wt <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - wt] + val)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find which parcels were selected
    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            parcel = parcels[i - 1]
            selected.append(parcel)
            w -= parcel["weight"]

    selected.reverse()
    total_weight = sum(p["weight"] for p in selected)
    total_value = dp[n][capacity]

    return {
        "selected_parcels": selected,
        "total_weight": total_weight,
        "remaining_capacity": capacity - total_weight,
        "total_value": total_value,
        "dp_table": dp,
    }