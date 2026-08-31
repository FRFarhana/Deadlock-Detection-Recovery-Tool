import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk

from graph import ResourceAllocationGraph
from deadlock_detection import DeadlockDetector
from deadlock_recovery import DeadlockRecovery

# Optional SDK
try:
    from sdk import DeadlockSDK
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False


# =========================================================
# SYSTEM DATA
# =========================================================

PROCESSES = ["P1", "P2", "P3", "P4", "P5"]

RESOURCES = [
    "R1", "R2", "R3", "R4", "R5",
    "R6", "R7", "R8", "R9", "R10"
]

PROCESS_COSTS = {
    "P1": 5,
    "P2": 4,
    "P3": 3,
    "P4": 2,
    "P5": 1
}


# =========================================================
# COLOR THEME
# =========================================================

BG = "#F4F7FB"
NAVY = "#172554"
BLUE = "#2563EB"
LIGHT_BLUE = "#DBEAFE"

GREEN = "#16A34A"
LIGHT_GREEN = "#DCFCE7"

RED = "#DC2626"
LIGHT_RED = "#FEE2E2"

ORANGE = "#EA580C"
LIGHT_ORANGE = "#FFEDD5"

PURPLE = "#7C3AED"
LIGHT_PURPLE = "#EDE9FE"

TEAL = "#0891B2"
LIGHT_TEAL = "#CFFAFE"

WHITE = "#FFFFFF"
DARK = "#1E293B"
GRAY = "#64748B"
LIGHT_GRAY = "#E2E8F0"


# =========================================================
# APPLICATION CLASS
# =========================================================

class DeadlockApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Deadlock Detection & Recovery Tool"
        )

        self.root.geometry("1200x780")
        self.root.minsize(1100, 720)

        self.root.configure(
            bg=BG
        )

        # Create initial system
        self.create_system()

        # Optional SDK
        self.sdk = None

        if SDK_AVAILABLE:
            try:
                self.sdk = DeadlockSDK(
                    PROCESSES,
                    RESOURCES,
                    PROCESS_COSTS
                )
            except Exception:
                self.sdk = None

        # Build GUI
        self.setup_styles()
        self.create_header()
        self.create_main_area()
        self.create_footer()

        self.update_dashboard()


    # =====================================================
    # SYSTEM CREATION
    # =====================================================

    def create_system(self):

        self.rag = ResourceAllocationGraph()

        # Add processes
        for process in PROCESSES:
            self.rag.add_process(process)

        # Add resources
        for resource in RESOURCES:
            self.rag.add_resource(resource)

        # Requests
        self.rag.request_resource("P1", "R1")
        self.rag.request_resource("P2", "R2")
        self.rag.request_resource("P3", "R3")
        self.rag.request_resource("P4", "R4")
        self.rag.request_resource("P5", "R5")

        # Deadlock allocations
        self.rag.allocate_resource("R1", "P2")
        self.rag.allocate_resource("R2", "P3")
        self.rag.allocate_resource("R3", "P4")
        self.rag.allocate_resource("R4", "P5")
        self.rag.allocate_resource("R5", "P1")

        # Additional allocations
        self.rag.allocate_resource("R6", "P1")
        self.rag.allocate_resource("R7", "P2")
        self.rag.allocate_resource("R8", "P3")
        self.rag.allocate_resource("R9", "P4")
        self.rag.allocate_resource("R10", "P5")


    # =====================================================
    # STYLES
    # =====================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=DARK,
            rowheight=30,
            fieldbackground=WHITE,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground=WHITE,
            font=("Arial", 10, "bold")
        )


    # =====================================================
    # HEADER
    # =====================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=NAVY,
            height=105
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        # Title
        tk.Label(
            header,
            text="DEADLOCK DETECTION & RECOVERY TOOL",
            bg=NAVY,
            fg=WHITE,
            font=("Arial", 25, "bold")
        ).pack(
            pady=(17, 3)
        )

        tk.Label(
            header,
            text=(
                "Resource Allocation Graph  •  "
                "Deadlock Detection  •  "
                "Recovery Management  •  SDK"
            ),
            bg=NAVY,
            fg="#CBD5E1",
            font=("Arial", 11)
        ).pack()


    # =====================================================
    # MAIN AREA
    # =====================================================

    def create_main_area(self):

        container = tk.Frame(
            self.root,
            bg=BG
        )

        container.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=18
        )

        # ================================================
        # LEFT SIDEBAR
        # ================================================

        sidebar = tk.Frame(
            container,
            bg=BG,
            width=265
        )

        sidebar.pack(
            side="left",
            fill="y",
            padx=(0, 15)
        )

        sidebar.pack_propagate(False)

        self.create_info_card(
            sidebar,
            "SYSTEM INFORMATION",
            BLUE,
            self.create_system_info
        )

        self.create_info_card(
            sidebar,
            "TERMINATION COST",
            PURPLE,
            self.create_cost_info
        )

        self.create_sdk_card(
            sidebar
        )

        # ================================================
        # RIGHT CONTENT
        # ================================================

        content = tk.Frame(
            container,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_status_card(
            content
        )

        self.create_cycle_card(
            content
        )

        self.create_recovery_card(
            content
        )

        self.create_operations_card(
            content
        )


    # =====================================================
    # INFO CARD
    # =====================================================

    def create_info_card(
        self,
        parent,
        title,
        accent,
        content_function
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Frame(
            card,
            bg=accent,
            height=5
        ).pack(
            fill="x"
        )

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=accent,
            font=("Arial", 11, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 8)
        )

        content_function(card)

        tk.Frame(
            card,
            height=8,
            bg=WHITE
        ).pack()


    # =====================================================
    # SYSTEM INFORMATION
    # =====================================================

    def create_system_info(self, parent):

        tk.Label(
            parent,
            text="PROCESSES",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 9, "bold")
        ).pack(
            anchor="w",
            padx=15
        )

        tk.Label(
            parent,
            text="   ".join(PROCESSES),
            bg=WHITE,
            fg=DARK,
            font=("Arial", 11, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(2, 10)
        )

        tk.Label(
            parent,
            text="RESOURCES",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 9, "bold")
        ).pack(
            anchor="w",
            padx=15
        )

        tk.Label(
            parent,
            text=(
                "R1  R2  R3  R4  R5\n"
                "R6  R7  R8  R9  R10"
            ),
            bg=WHITE,
            fg=DARK,
            font=("Arial", 10, "bold"),
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(2, 10)
        )

        self.active_label = tk.Label(
            parent,
            text="ACTIVE PROCESSES\n5 / 5",
            bg=LIGHT_GREEN,
            fg=GREEN,
            font=("Arial", 11, "bold"),
            justify="center",
            padx=15,
            pady=10
        )

        self.active_label.pack(
            fill="x",
            padx=12
        )


    # =====================================================
    # COST INFORMATION
    # =====================================================

    def create_cost_info(self, parent):

        for process in PROCESSES:

            row = tk.Frame(
                parent,
                bg=WHITE
            )

            row.pack(
                fill="x",
                padx=15,
                pady=2
            )

            tk.Label(
                row,
                text=process,
                bg=WHITE,
                fg=DARK,
                font=("Arial", 10, "bold"),
                width=5,
                anchor="w"
            ).pack(
                side="left"
            )

            tk.Label(
                row,
                text=f"→ Cost {PROCESS_COSTS[process]}",
                bg=WHITE,
                fg=GRAY,
                font=("Arial", 10)
            ).pack(
                side="left"
            )


    # =====================================================
    # SDK CARD
    # =====================================================

    def create_sdk_card(self, parent):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Frame(
            card,
            bg=TEAL,
            height=5
        ).pack(
            fill="x"
        )

        tk.Label(
            card,
            text="SDK STATUS",
            bg=WHITE,
            fg=TEAL,
            font=("Arial", 11, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        sdk_status = (
            "● CONNECTED"
            if self.sdk
            else "● LOCAL MODE"
        )

        sdk_color = (
            GREEN
            if self.sdk
            else GRAY
        )

        tk.Label(
            card,
            text=sdk_status,
            bg=WHITE,
            fg=sdk_color,
            font=("Arial", 10, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 5)
        )

        tk.Label(
            card,
            text="Deadlock SDK\nAPI Integration Layer",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 9),
            justify="left"
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )


    # =====================================================
    # STATUS CARD
    # =====================================================

    def create_status_card(self, parent):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(0, 12)
        )

        self.status_indicator = tk.Label(
            card,
            text="●",
            bg=WHITE,
            fg=GREEN,
            font=("Arial", 22)
        )

        self.status_indicator.pack(
            pady=(12, 0)
        )

        tk.Label(
            card,
            text="SYSTEM STATUS",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 9, "bold")
        ).pack()

        self.status_value = tk.Label(
            card,
            text="SYSTEM READY",
            bg=WHITE,
            fg=GREEN,
            font=("Arial", 17, "bold")
        )

        self.status_value.pack(
            pady=(3, 14)
        )


    # =====================================================
    # CYCLE CARD
    # =====================================================

    def create_cycle_card(self, parent):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(0, 12)
        )

        top = tk.Frame(
            card,
            bg=LIGHT_RED
        )

        top.pack(
            fill="x"
        )

        self.cycle_title = tk.Label(
            top,
            text="⚠  DEADLOCK CYCLE",
            bg=LIGHT_RED,
            fg=RED,
            font=("Arial", 11, "bold")
        )

        self.cycle_title.pack(
            pady=(10, 3)
        )

        self.cycle_value = tk.Label(
            card,
            text="No detection performed yet.",
            bg=WHITE,
            fg=DARK,
            font=("Arial", 11, "bold"),
            wraplength=750,
            justify="center"
        )

        self.cycle_value.pack(
            padx=20,
            pady=12
        )


    # =====================================================
    # RECOVERY CARD
    # =====================================================

    def create_recovery_card(self, parent):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            card,
            text="RECOVERY STATUS",
            bg=WHITE,
            fg=ORANGE,
            font=("Arial", 10, "bold")
        ).pack(
            pady=(11, 3)
        )

        self.recovery_value = tk.Label(
            card,
            text="No recovery performed.",
            bg=WHITE,
            fg=GRAY,
            font=("Arial", 10)
        )

        self.recovery_value.pack(
            pady=(0, 12)
        )


    # =====================================================
    # BUTTON HELPER
    # =====================================================

    def create_button(
        self,
        parent,
        text,
        command,
        color,
        width=22
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            height=2,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            cursor="hand2",
            font=("Arial", 10, "bold")
        )

        button.pack(
            side="left",
            padx=6,
            pady=5
        )

        return button


    # =====================================================
    # OPERATIONS
    # =====================================================

    def create_operations_card(self, parent):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=LIGHT_GRAY,
            highlightthickness=1
        )

        card.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            card,
            text="OPERATIONS",
            bg=WHITE,
            fg=NAVY,
            font=("Arial", 12, "bold")
        ).pack(
            pady=(15, 8)
        )

        row1 = tk.Frame(
            card,
            bg=WHITE
        )

        row1.pack()

        self.create_button(
            row1,
            "SHOW RESOURCE GRAPH",
            self.show_graph,
            BLUE
        )

        self.create_button(
            row1,
            "DETECT DEADLOCK",
            self.detect_deadlock,
            RED
        )

        row2 = tk.Frame(
            card,
            bg=WHITE
        )

        row2.pack()

        self.create_button(
            row2,
            "TERMINATE PROCESS",
            self.terminate_process,
            ORANGE
        )

        self.create_button(
            row2,
            "RESOURCE PREEMPTION",
            self.resource_preemption,
            TEAL
        )

        row3 = tk.Frame(
            card,
            bg=WHITE
        )

        row3.pack()

        self.create_button(
            row3,
            "RESET SYSTEM",
            self.reset_system,
            GREEN
        )

        self.create_button(
            row3,
            "LOWEST-COST RECOVERY",
            self.lowest_cost_recovery,
            PURPLE
        )

        row4 = tk.Frame(
            card,
            bg=WHITE
        )

        row4.pack(
            pady=(3, 8)
        )

        self.create_button(
            row4,
            "EXIT APPLICATION",
            self.root.destroy,
            NAVY,
            width=30
        )


    # =====================================================
    # FOOTER
    # =====================================================

    def create_footer(self):

        footer = tk.Frame(
            self.root,
            bg=NAVY,
            height=35
        )

        footer.pack(
            fill="x"
        )

        footer.pack_propagate(False)

        tk.Label(
            footer,
            text=(
                "OS Project  •  RAG  •  DFS Cycle Detection  •  "
                "Process Termination  •  Resource Preemption  •  SDK"
            ),
            bg=NAVY,
            fg="#CBD5E1",
            font=("Arial", 9)
        ).pack(
            pady=9
        )


    # =====================================================
    # UPDATE DASHBOARD
    # =====================================================

    def update_dashboard(self):

        active = [
            p for p in PROCESSES
            if p in self.rag.graph.nodes
        ]

        count = len(active)

        self.active_label.config(
            text=f"ACTIVE PROCESSES\n{count} / {len(PROCESSES)}"
        )


    # =====================================================
    # DETECT DEADLOCK
    # =====================================================

    def detect_deadlock(self):

        detector = DeadlockDetector(
            self.rag.graph
        )

        found = detector.detect_deadlock()

        if found:

            cycle = detector.get_deadlock_cycle()

            cycle_text = "  →  ".join(cycle)

            self.status_indicator.config(
                fg=RED
            )

            self.status_value.config(
                text="DEADLOCK DETECTED",
                fg=RED
            )

            self.cycle_value.config(
                text=cycle_text,
                fg=RED
            )

            self.recovery_value.config(
                text="⚠ Recovery action required.",
                fg=ORANGE
            )

            messagebox.showwarning(
                "Deadlock Detected",
                "Deadlock detected!\n\n"
                + cycle_text
            )

        else:

            self.status_indicator.config(
                fg=GREEN
            )

            self.status_value.config(
                text="SYSTEM SAFE",
                fg=GREEN
            )

            self.cycle_value.config(
                text="No deadlock cycle found.",
                fg=GREEN
            )

            self.recovery_value.config(
                text="System is currently safe.",
                fg=GREEN
            )

            messagebox.showinfo(
                "Deadlock Detection",
                "No deadlock detected."
            )


    # =====================================================
    # SHOW GRAPH
    # =====================================================

    def show_graph(self):

        self.rag.show_graph()


    # =====================================================
    # TERMINATE PROCESS
    # =====================================================

    def terminate_process(self):

        process = simpledialog.askstring(
            "Process Termination",
            "Enter process:\nP1, P2, P3, P4, P5"
        )

        if not process:
            return

        process = process.strip().upper()

        if process not in PROCESSES:

            messagebox.showerror(
                "Invalid Process",
                "Enter P1, P2, P3, P4 or P5."
            )

            return

        if process not in self.rag.graph.nodes:

            messagebox.showerror(
                "Process Not Available",
                f"{process} has already been terminated."
            )

            return

        recovery = DeadlockRecovery(
            self.rag.graph
        )

        success = recovery.recover_by_termination(
            process
        )

        if success:

            self.status_value.config(
                text=f"{process} TERMINATED",
                fg=ORANGE
            )

            self.status_indicator.config(
                fg=ORANGE
            )

            self.recovery_value.config(
                text=f"✓ Process {process} terminated successfully.",
                fg=GREEN
            )

            self.update_dashboard()

            messagebox.showinfo(
                "Recovery Successful",
                f"{process} was terminated successfully."
            )

            self.rag.show_graph()


    # =====================================================
    # RESOURCE PREEMPTION
    # =====================================================

    def resource_preemption(self):

        resource = simpledialog.askstring(
            "Resource Preemption",
            "Enter resource:\nR1 - R10"
        )

        if not resource:
            return

        resource = resource.strip().upper()

        holder = simpledialog.askstring(
            "Resource Preemption",
            "Enter current holder:\nP1 - P5"
        )

        if not holder:
            return

        holder = holder.strip().upper()

        requester = simpledialog.askstring(
            "Resource Preemption",
            "Enter requesting process:\nP1 - P5"
        )

        if not requester:
            return

        requester = requester.strip().upper()

        recovery = DeadlockRecovery(
            self.rag.graph
        )

        success = recovery.recover_by_preemption(
            resource,
            holder,
            requester
        )

        if success:

            self.status_indicator.config(
                fg=TEAL
            )

            self.status_value.config(
                text="RESOURCE PREEMPTED",
                fg=TEAL
            )

            self.recovery_value.config(
                text=(
                    f"✓ {resource} moved from "
                    f"{holder} → {requester}"
                ),
                fg=GREEN
            )

            messagebox.showinfo(
                "Preemption Successful",
                f"{resource} was preempted from "
                f"{holder} and allocated to "
                f"{requester}."
            )

            self.rag.show_graph()

        else:

            messagebox.showerror(
                "Preemption Failed",
                "Invalid resource, holder, requester "
                "or relationship."
            )


    # =====================================================
    # LOWEST COST RECOVERY
    # =====================================================

    def lowest_cost_recovery(self):

        active_processes = [
            p for p in PROCESSES
            if p in self.rag.graph.nodes
        ]

        if not active_processes:

            messagebox.showerror(
                "Recovery Error",
                "No active processes available."
            )

            return

        lowest_process = min(
            active_processes,
            key=lambda p: PROCESS_COSTS[p]
        )

        lowest_cost = PROCESS_COSTS[
            lowest_process
        ]

        answer = messagebox.askyesno(
            "Lowest-Cost Recovery",
            f"Lowest-cost process: {lowest_process}\n"
            f"Termination cost: {lowest_cost}\n\n"
            f"Terminate {lowest_process}?"
        )

        if not answer:
            return

        recovery = DeadlockRecovery(
            self.rag.graph
        )

        success = recovery.recover_by_termination(
            lowest_process
        )

        if success:

            self.status_indicator.config(
                fg=PURPLE
            )

            self.status_value.config(
                text="LOWEST-COST RECOVERY",
                fg=PURPLE
            )

            self.recovery_value.config(
                text=(
                    f"✓ {lowest_process} terminated "
                    f"(cost = {lowest_cost})"
                ),
                fg=GREEN
            )

            self.update_dashboard()

            messagebox.showinfo(
                "Lowest-Cost Recovery",
                f"Process {lowest_process} terminated.\n"
                f"Termination Cost = {lowest_cost}"
            )

            self.rag.show_graph()


    # =====================================================
    # RESET SYSTEM
    # =====================================================

    def reset_system(self):

        answer = messagebox.askyesno(
            "Reset System",
            "Reset the entire system?\n\n"
            "All terminated processes and recovery "
            "changes will be restored."
        )

        if not answer:
            return

        self.create_system()

        self.status_indicator.config(
            fg=GREEN
        )

        self.status_value.config(
            text="SYSTEM READY",
            fg=GREEN
        )

        self.cycle_value.config(
            text="No detection performed yet.",
            fg=DARK
        )

        self.recovery_value.config(
            text="No recovery performed.",
            fg=GRAY
        )

        self.update_dashboard()

        messagebox.showinfo(
            "System Reset",
            "System has been successfully reset."
        )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = DeadlockApp(root)

    root.mainloop()