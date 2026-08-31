from graph import ResourceAllocationGraph
from deadlock_detection import DeadlockDetector
from deadlock_recovery import DeadlockRecovery


# =========================================================
# CREATE RESOURCE ALLOCATION GRAPH
# =========================================================

rag = ResourceAllocationGraph()


# =========================================================
# ADD PROCESSES
# =========================================================

processes = [
    "P1",
    "P2",
    "P3",
    "P4",
    "P5"
]

for process in processes:
    rag.add_process(process)


# =========================================================
# ADD 10 RESOURCES
# =========================================================

resources = [
    "R1", "R2", "R3", "R4", "R5",
    "R6", "R7", "R8", "R9", "R10"
]

for resource in resources:
    rag.add_resource(resource)


# =========================================================
# CREATE RESOURCE REQUESTS
# Process -> Resource
# =========================================================

rag.request_resource("P1", "R1")
rag.request_resource("P2", "R2")
rag.request_resource("P3", "R3")
rag.request_resource("P4", "R4")
rag.request_resource("P5", "R5")


# =========================================================
# ALLOCATE RESOURCES
# Resource -> Process
#
# DEADLOCK CYCLE:
#
# P1 → R1 → P2 → R2 → P3 → R3
# → P4 → R4 → P5 → R5 → P1
# =========================================================

rag.allocate_resource("R1", "P2")
rag.allocate_resource("R2", "P3")
rag.allocate_resource("R3", "P4")
rag.allocate_resource("R4", "P5")
rag.allocate_resource("R5", "P1")


# =========================================================
# ADDITIONAL RESOURCE ALLOCATIONS
# =========================================================

rag.allocate_resource("R6", "P1")
rag.allocate_resource("R7", "P2")
rag.allocate_resource("R8", "P3")
rag.allocate_resource("R9", "P4")
rag.allocate_resource("R10", "P5")


# =========================================================
# PROCESS TERMINATION COSTS
#
# Lower value = lower termination cost
# =========================================================

process_costs = {
    "P1": 5,
    "P2": 4,
    "P3": 3,
    "P4": 2,
    "P5": 1
}


# =========================================================
# SHOW ORIGINAL GRAPH
# =========================================================

print("\n")
print("====================================================")
print("          RESOURCE ALLOCATION GRAPH")
print("====================================================")

rag.show_graph()


# =========================================================
# DEADLOCK DETECTION
# =========================================================

detector = DeadlockDetector(rag.graph)

deadlock_found = detector.detect_deadlock()


# =========================================================
# RECOVERY
# =========================================================

if deadlock_found:

    recovery = DeadlockRecovery(rag.graph)

    print("\n")
    print("====================================================")
    print("                RECOVERY OPTIONS")
    print("====================================================")

    print("1. Terminate P1")
    print("2. Terminate P2")
    print("3. Terminate P3")
    print("4. Terminate P4")
    print("5. Terminate P5")
    print("6. Resource Preemption")
    print("7. Terminate Lowest-Cost Process")

    choice = input(
        "\nEnter your choice (1-7): "
    ).strip()


    # =====================================================
    # TERMINATE P1
    # =====================================================

    if choice == "1":

        recovery.recover_by_termination("P1")


    # =====================================================
    # TERMINATE P2
    # =====================================================

    elif choice == "2":

        recovery.recover_by_termination("P2")


    # =====================================================
    # TERMINATE P3
    # =====================================================

    elif choice == "3":

        recovery.recover_by_termination("P3")


    # =====================================================
    # TERMINATE P4
    # =====================================================

    elif choice == "4":

        recovery.recover_by_termination("P4")


    # =====================================================
    # TERMINATE P5
    # =====================================================

    elif choice == "5":

        recovery.recover_by_termination("P5")


    # =====================================================
    # RESOURCE PREEMPTION
    # =====================================================

    elif choice == "6":

        print("\n")
        print("====================================================")
        print("              RESOURCE PREEMPTION")
        print("====================================================")

        print("\nAvailable resources:")
        print(", ".join(resources))

        resource = input(
            "\nEnter resource to preempt: "
        ).strip().upper()

        holder = input(
            "Enter current resource holder: "
        ).strip().upper()

        requester = input(
            "Enter requesting process: "
        ).strip().upper()

        recovery.recover_by_preemption(
            resource,
            holder,
            requester
        )


    # =====================================================
    # LOWEST-COST PROCESS TERMINATION
    # =====================================================

    elif choice == "7":

        print("\n")
        print("====================================================")
        print("        LOWEST-COST PROCESS TERMINATION")
        print("====================================================")

        active_processes = [
            process
            for process in processes
            if process in rag.graph.nodes
        ]

        if not active_processes:

            print("No active processes available.")

        else:

            print("\nProcess termination costs:")

            for process in active_processes:

                print(
                    f"{process} = "
                    f"{process_costs[process]}"
                )

            # Find lowest-cost process
            lowest_cost_process = min(
                active_processes,
                key=lambda process: process_costs[process]
            )

            lowest_cost = process_costs[
                lowest_cost_process
            ]

            print(
                f"\nLowest-cost process: "
                f"{lowest_cost_process}"
            )

            print(
                f"Termination cost: "
                f"{lowest_cost}"
            )

            recovery.recover_by_termination(
                lowest_cost_process
            )


    # =====================================================
    # INVALID CHOICE
    # =====================================================

    else:

        print("\nInvalid choice!")
        print("Please select an option from 1 to 7.")


    # =====================================================
    # CHECK DEADLOCK AGAIN AFTER RECOVERY
    # =====================================================

    print("\n")
    print("====================================================")
    print("          DEADLOCK STATUS AFTER RECOVERY")
    print("====================================================")

    detector_after_recovery = DeadlockDetector(
        rag.graph
    )

    still_deadlocked = (
        detector_after_recovery.detect_deadlock()
    )


    # =====================================================
    # RECOVERY SUMMARY
    # =====================================================

    summary = recovery.get_recovery_summary()

    print("\n")
    print("====================================================")
    print("                 RECOVERY SUMMARY")
    print("====================================================")

    print("\nDeadlock detected: YES")

    print("\nOriginal Deadlock Cycle:")

    original_cycle = detector.get_deadlock_cycle()

    if original_cycle:

        print(
            " → ".join(original_cycle)
        )

    else:

        print("Cycle information unavailable.")


    # =====================================================
    # SHOW RECOVERY METHOD
    # =====================================================

    print("\nRecovery Method:")

    if summary["method"]:

        print(summary["method"])

    else:

        print("None")


    # =====================================================
    # PROCESS TERMINATION SUMMARY
    # =====================================================

    if summary["method"] == "Process Termination":

        print("\nTerminated Process:")

        print(summary["process"])


    # =====================================================
    # RESOURCE PREEMPTION SUMMARY
    # =====================================================

    elif summary["method"] == "Resource Preemption":

        print("\nPreempted Resource:")

        print(summary["resource"])

        print("Previous Holder:")

        print(summary["holder"])

        print("New Holder:")

        print(summary["requester"])


    # =====================================================
    # RECOVERY STATUS
    # =====================================================

    print("\nRecovery Status:")

    if summary["success"]:

        print("SUCCESS")

    else:

        print("FAILED")


    # =====================================================
    # FINAL DEADLOCK STATUS
    # =====================================================

    print("\nDeadlock After Recovery:")

    if still_deadlocked:

        print(
            "YES — Deadlock still exists."
        )

    else:

        print(
            "NO — Deadlock successfully recovered."
        )


    print("\n====================================================")


    # =====================================================
    # SHOW RECOVERED GRAPH
    # =====================================================

    print("\n")
    print("====================================================")
    print("                RECOVERED GRAPH")
    print("====================================================")

    rag.show_graph()


# =========================================================
# NO DEADLOCK
# =========================================================

else:

    print("\n")
    print("====================================================")
    print("             NO DEADLOCK DETECTED")
    print("====================================================")

    print(
        "The Resource Allocation Graph contains no cycle."
    )