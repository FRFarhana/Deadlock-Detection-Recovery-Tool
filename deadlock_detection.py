class DeadlockDetector:

    def __init__(self, graph):
        self.graph = graph
        self.deadlock_cycle = []

    # =====================================================
    # DFS
    # =====================================================

    def _dfs(self, node, visited, recursion_stack, path):

        visited.add(node)
        recursion_stack.add(node)
        path.append(node)

        for neighbor in self.graph.successors(node):

            if neighbor not in visited:

                cycle = self._dfs(
                    neighbor,
                    visited,
                    recursion_stack,
                    path
                )

                if cycle:
                    return cycle

            elif neighbor in recursion_stack:

                start_index = path.index(neighbor)

                return path[start_index:] + [neighbor]

        recursion_stack.remove(node)
        path.pop()

        return None

    # =====================================================
    # DETECT DEADLOCK
    # =====================================================

    def detect_deadlock(self):

        self.deadlock_cycle = []

        visited = set()
        recursion_stack = set()

        for node in self.graph.nodes:

            if node not in visited:

                cycle = self._dfs(
                    node,
                    visited,
                    recursion_stack,
                    []
                )

                if cycle:

                    self.deadlock_cycle = cycle

                    print("\n==============================================")
                    print("            DEADLOCK DETECTED")
                    print("==============================================")

                    print("\nExact Deadlock Cycle:")
                    print(" → ".join(cycle))

                    processes = [
                        item for item in cycle
                        if str(item).startswith("P")
                    ]

                    print("\nDeadlocked Processes:")
                    print(", ".join(processes))

                    return True

        print("\n==============================================")
        print("             NO DEADLOCK DETECTED")
        print("==============================================")

        return False

    # =====================================================
    # GET DEADLOCK CYCLE
    # =====================================================

    def get_deadlock_cycle(self):

        return self.deadlock_cycle