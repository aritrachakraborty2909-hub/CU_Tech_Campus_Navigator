# CU_Tech_Campus_Navigator
AI-based campus navigation system for CU Technology Campus using Greedy Best-First Search and A* pathfinding algorithms with custom zone routing rules.

### Strategy
1. **Graph Representation**: The map was translated into an undirected weighted graph in `campus.json` containing nodes and approximate path lengths in meters.
2. **Distance-Based Heuristic**: $h(n)$ is calculated via shortest distance edge-weights to the target node.
3. **CSE Zone Enforcement**: Transition constraints guarantee that CSE rooms are entered and exited strictly via `Lift Area -> Tower 2 Entry`.
4. **Agent Comparison**: PATHFINDER ($f=h$) acts greedily, while ORBIT ($f=g+h$) guarantees optimal path selection.