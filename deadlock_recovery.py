class DeadlockRecovery:

    def __init__(self, graph):
        self.graph = graph
        self.last_recovery = {
            "method": None,
            "process": None,
            "resource": None,
            "holder": None,
            "requester": None,
            "success": False
        }

    # =====================================================
    # PROCESS TERMINATION
    # =====================================================

    def recover_by_termination(self, process):

        self.last_recovery = {
            "method": "Process Termination",
            "process": process,
            "resource": None,
            "holder": None,
            "requester": None,
            "success": False
        }

        print("\n==============================================")
        print("             PROCESS TERMINATION")
        print("==============================================")

        if process not in self.graph.nodes:
            print(f"Process {process} was not found.")
            return False

        print(f"\nTerminating process: {process}")

        self.graph.remove_node(process)

        self.last_recovery["success"] = True

        print(f"Process {process} terminated.")
        print("Related requests and allocations were removed.")
        print("\nRecovery operation completed.")

        return True

    # =====================================================
    # RESOURCE PREEMPTION
    # =====================================================

    def recover_by_preemption(
        self,
        resource,
        holder,
        requester
    ):

        self.last_recovery = {
            "method": "Resource Preemption",
            "process": None,
            "resource": resource,
            "holder": holder,
            "requester": requester,
            "success": False
        }

        print("\n==============================================")
        print("             RESOURCE PREEMPTION")
        print("==============================================")

        if resource not in self.graph.nodes:
            print(f"Resource {resource} was not found.")
            return False

        if holder not in self.graph.nodes:
            print(f"Process {holder} was not found.")
            return False

        if requester not in self.graph.nodes:
            print(f"Process {requester} was not found.")
            return False

        if not self.graph.has_edge(resource, holder):
            print(
                f"{resource} is not currently allocated "
                f"to {holder}."
            )
            return False

        if not self.graph.has_edge(requester, resource):
            print(
                f"{requester} is not requesting "
                f"{resource}."
            )
            return False

        # Remove old allocation
        self.graph.remove_edge(resource, holder)

        # Remove request
        self.graph.remove_edge(requester, resource)

        # Allocate resource to requester
        self.graph.add_edge(
            resource,
            requester,
            edge_type="allocation"
        )

        self.last_recovery["success"] = True

        print(
            f"\nResource {resource} preempted from {holder}."
        )

        print(
            f"Resource {resource} allocated to {requester}."
        )

        print("\nRecovery completed successfully.")

        return True

    # =====================================================
    # GET RECOVERY INFORMATION
    # =====================================================

    def get_recovery_summary(self):

        return self.last_recovery