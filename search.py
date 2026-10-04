import heapq
import time

class SearchEngine:
    def __init__(self, campus_map):
        self.campus = campus_map

    def search(self, start, goal, algorithm="A*"):
        start_time = time.perf_counter()
        
        # Determine starting CSE state
        initial_cse = start in {"CSE_Lab", "CSE_Reflexon", "CSE_Seminar"}
        
        frontier = []
        counter = 0
        
        h0 = self.campus.get_heuristic(start, goal)
        f0 = h0 if algorithm == "Greedy" else h0
        
        # State: (f, counter, current_node, in_cse_zone, path, g_cost)
        heapq.heappush(frontier, (f0, counter, start, initial_cse, [start], 0))
        
        visited = {}
        nodes_explored = 0

        while frontier:
            f, _, curr_node, in_cse, path, g = heapq.heappop(frontier)
            
            state = (curr_node, in_cse)
            if state in visited and visited[state] <= g:
                continue
            visited[state] = g
            nodes_explored += 1

            if curr_node == goal:
                exec_time = time.perf_counter() - start_time
                return path, g, nodes_explored, exec_time

            for neighbor, weight in self.campus.adj[curr_node]:
                # Check transition validity under current CSE state
                if not self.campus.is_valid_transition(curr_node, neighbor, in_cse):
                    continue
                
                # Determine state AFTER step is taken
                if neighbor in {"CSE_Lab", "CSE_Reflxon", "CSE_Seminar"}:
                    next_in_cse = True
                elif neighbor == "LiftArea" and in_cse:
                    next_in_cse = False  # Exiting CSE zone
                else:
                    next_in_cse = in_cse

                next_g = g + weight
                h = self.campus.get_heuristic(neighbor, goal)
                next_f = h if algorithm == "Greedy" else (next_g + h)
                
                counter += 1
                heapq.heappush(frontier, (next_f, counter, neighbor, next_in_cse, path + [neighbor], next_g))

        exec_time = time.perf_counter() - start_time
        return None, float("inf"), nodes_explored, exec_time