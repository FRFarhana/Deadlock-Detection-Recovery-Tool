"""
Deadlock Detection & Recovery SDK
---------------------------------
A simple SDK layer for the Deadlock Detection & Recovery Tool.

It provides:
    - Resource Allocation Graph creation
    - Deadlock detection
    - Exact deadlock cycle retrieval
    - Process termination
    - Resource preemption
    - Lowest-cost recovery
    - System reset
    - System status and summary
"""

from graph import ResourceAllocationGraph
from deadlock_detection import DeadlockDetector
from deadlock_recovery import DeadlockRecovery


class DeadlockSDK:

    # =====================================================
    # DEFAULT PROJECT DATA
    # =====================================================

    DEFAULT_PROCESSES = [
        "P1",
        "P2",
        "P3",
        "P4",
        "P5"
    ]

    DEFAULT_RESOURCES = [
        "R1",
        "R2",
        "R3",
        "R4",
        "R5",
        "R6",
        "R7",
        "R8",
        "R9",
        "R10"
    ]

    DEFAULT_PROCESS_COSTS = {
        "P1": 5,
        "P2": 4,
        "P3": 3,
        "P4": 2,
        "P5": 1
    }

    # =====================================================
    # INITIALIZATION
    # =====================================================

    def __init__(
        self,
        processes=None,
        resources=None,
        process_costs=None
    ):

        self.processes = list(
            processes
            if processes is not None
            else self.DEFAULT_PROCESSES
        )

        self.resources = list(
            resources
            if resources is not None
            else self.DEFAULT_RESOURCES
        )

        self.process_costs = dict(
            process_costs
            if process_costs is not None
            else self.DEFAULT_PROCESS_COSTS
        )

        self.rag = None

        self.reset()

    # =====================================================
    # RESET SYSTEM
    # =====================================================

    def reset(self):

        self.rag = ResourceAllocationGraph()

        # Add processes
        for process in self.processes:
            self.rag.add_process(process)

        # Add resources
        for resource in self.resources:
            self.rag.add_resource(resource)

        # -------------------------------------------------
        # Create Deadlock
        #
        # P1 -> R1 -> P2
        # P2 -> R2 -> P3
        # P3 -> R3 -> P4
        # P4 -> R4 -> P5
        # P5 -> R5 -> P1
        # -------------------------------------------------

        self.rag.request_resource("P1", "R1")
        self.rag.request_resource("P2", "R2")
        self.rag.request_resource("P3", "R3")
        self.rag.request_resource("P4", "R4")
        self.rag.request_resource("P5", "R5")

        self.rag.allocate_resource("R1", "P2")
        self.rag.allocate_resource("R2", "P3")
        self.rag.allocate_resource("R3", "P4")
        self.rag.allocate_resource("R4", "P5")
        self.rag.allocate_resource("R5", "P1")

        # Additional resources
        self.rag.allocate_resource("R6", "P1")
        self.rag.allocate_resource("R7", "P2")
        self.rag.allocate_resource("R8", "P3")
        self.rag.allocate_resource("R9", "P4")
        self.rag.allocate_resource("R10", "P5")

        return self.rag

    # =====================================================
    # GET GRAPH
    # =====================================================

    def get_graph(self):

        return self.rag.graph

    # =====================================================
    # DETECT DEADLOCK
    # =====================================================

    def detect_deadlock(self):

        detector = DeadlockDetector(
            self.rag.graph
        )

        found = detector.detect_deadlock()

        cycle = []

        if found:

            cycle = detector.get_deadlock_cycle()

        return found, cycle

    # =====================================================
    # GET DEADLOCK CYCLE
    # =====================================================

    def get_deadlock_cycle(self):

        detector = DeadlockDetector(
            self.rag.graph
        )

        if detector.detect_deadlock():

            return detector.get_deadlock_cycle()

        return []

    # =====================================================
    # SHOW GRAPH
    # =====================================================

    def show_graph(self):

        self.rag.show_graph()

    # =====================================================
    # TERMINATE PROCESS
    # =====================================================

    def terminate_process(self, process):

        process = process.strip().upper()

        if process not in self.processes:
            return False, "Invalid process."

        if process not in self.rag.graph.nodes:
            return False, (
                f"{process} is already terminated."
            )

        recovery = DeadlockRecovery(
            self.rag.graph
        )

        success = recovery.recover_by_termination(
            process
        )

        if success:

            return True, (
                f"Process {process} terminated successfully."
            )

        return False, (
            f"Failed to terminate {process}."
        )

    # =====================================================
    # RESOURCE PREEMPTION
    # =====================================================

    def preempt_resource(
        self,
        resource,
        holder,
        requester
    ):

        resource = resource.strip().upper()
        holder = holder.strip().upper()
        requester = requester.strip().upper()

        if resource not in self.resources:

            return False, (
                f"Invalid resource: {resource}"
            )

        if holder not in self.processes:

            return False, (
                f"Invalid holder: {holder}"
            )

        if requester not in self.processes:

            return False, (
                f"Invalid requester: {requester}"
            )

        if holder not in self.rag.graph.nodes:

            return False, (
                f"{holder} is not active."
            )

        if requester not in self.rag.graph.nodes:

            return False, (
                f"{requester} is not active."
            )

        recovery = DeadlockRecovery(
            self.rag.graph
        )

        success = recovery.recover_by_preemption(
            resource,
            holder,
            requester
        )

        if success:

            return True, (
                f"{resource} was preempted from "
                f"{holder} and allocated to "
                f"{requester}."
            )

        return False, (
            "Resource preemption failed. "
            "Check the resource, holder and requester."
        )

    # =====================================================
    # LOWEST-COST PROCESS
    # =====================================================

    def get_lowest_cost_process(self):

        active_processes = [
            process
            for process in self.processes
            if process in self.rag.graph.nodes
        ]

        if not active_processes:

            return None, None

        lowest_process = min(
            active_processes,
            key=lambda process:
            self.process_costs.get(
                process,
                999999
            )
        )

        lowest_cost = self.process_costs.get(
            lowest_process,
            0
        )

        return lowest_process, lowest_cost

    # =====================================================
    # LOWEST-COST RECOVERY
    # =====================================================

    def lowest_cost_recovery(self):

        process, cost = (
            self.get_lowest_cost_process()
        )

        if process is None:

            return False, (
                "No active processes available."
            )

        success, message = (
            self.terminate_process(process)
        )

        if success:

            return True, (
                f"{process} terminated using "
                f"lowest-cost recovery. "
                f"Cost = {cost}"
            )

        return False, message

    # =====================================================
    # ACTIVE PROCESSES
    # =====================================================

    def get_active_processes(self):

        return [
            process
            for process in self.processes
            if process in self.rag.graph.nodes
        ]

    # =====================================================
    # ACTIVE PROCESS COUNT
    # =====================================================

    def get_active_process_count(self):

        return len(
            self.get_active_processes()
        )

    # =====================================================
    # SYSTEM STATUS
    # =====================================================

    def get_status(self):

        found, cycle = (
            self.detect_deadlock()
        )

        if found:

            return "DEADLOCK DETECTED"

        return "SYSTEM SAFE"

    # =====================================================
    # SDK SUMMARY
    # =====================================================

    def get_summary(self):

        found, cycle = (
            self.detect_deadlock()
        )

        active = (
            self.get_active_processes()
        )

        summary = {
            "total_processes":
                len(self.processes),

            "active_processes":
                len(active),

            "total_resources":
                len(self.resources),

            "deadlock":
                found,

            "cycle":
                cycle,

            "status":
                self.get_status()
        }

        return summary


# =========================================================
# SDK TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DEADLOCK DETECTION & RECOVERY SDK TEST")
    print("=" * 60)

    sdk = DeadlockSDK()

    print("\nProcesses:")
    print(sdk.processes)

    print("\nResources:")
    print(sdk.resources)

    print("\nActive Processes:")
    print(sdk.get_active_processes())

    print("\nSystem Status:")
    print(sdk.get_status())

    found, cycle = (
        sdk.detect_deadlock()
    )

    print("\nDeadlock:")
    print(found)

    if found:

        print("\nExact Deadlock Cycle:")

        print(
            " -> ".join(cycle)
        )

    lowest_process, lowest_cost = (
        sdk.get_lowest_cost_process()
    )

    print("\nLowest-Cost Process:")
    print(
        lowest_process,
        "Cost =",
        lowest_cost
    )

    print("\nSDK Summary:")
    print(
        sdk.get_summary()
    )

    print("=" * 60)
    print("SDK TEST COMPLETED")
    print("=" * 60)