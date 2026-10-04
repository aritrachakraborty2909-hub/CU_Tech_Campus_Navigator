import json
import heapq

CSE_LOCATIONS = {"CSE_Lab", "CSE_Reflexon", "CSE_Seminar"}

class CampusMap:
    def __init__(self, json_path="campus.json"):
        with open(json_path, "r") as f:
            data = json.load(f)
        
        self.nodes = data["locations"]
        self.adj = {k: [] for k in self.nodes}
        
        for conn in data["connections"]:
            u, v, w = conn["from"], conn["to"], conn["weight"]
            self.adj[u].append((v, w))
            self.adj[v].append((u, w))

    def get_heuristic(self, node, goal):
        """Pure unconstrained shortest path distance for h(n)."""
        if node == goal:
            return 0

        distances = {k: float("inf") for k in self.nodes}
        distances[node] = 0
        pq = [(0, node)]

        while pq:
            curr_d, curr_n = heapq.heappop(pq)
            if curr_n == goal:
                return curr_d

            if curr_d > distances[curr_n]:
                continue

            for neighbor, weight in self.adj[curr_n]:
                if curr_d + weight < distances[neighbor]:
                    distances[neighbor] = curr_d + weight
                    heapq.heappush(pq, (distances[neighbor], neighbor))

        return distances[goal] if distances[goal] != float("inf") else 0

    def is_valid_transition(self, current_node, next_node, in_cse_zone):
        """
        Part 7 Rule:
        1. If already inside the CSE zone, you can ONLY move to another CSE location or exit to Lift Area.
        2. You CANNOT jump into a CSE location directly from general campus (must go through Lift Area).
        """
        if in_cse_zone:
            # Inside CSE zone: allowed next nodes are CSE rooms or LiftArea (to exit)
            return next_node in CSE_LOCATIONS or next_node == "LiftArea"

        # Outside CSE zone: direct jumps into CSE rooms are blocked unless you are at LiftArea
        if next_node in CSE_LOCATIONS:
            return current_node == "LiftArea"

        return True