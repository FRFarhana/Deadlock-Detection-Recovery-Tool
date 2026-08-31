import networkx as nx
import matplotlib.pyplot as plt


class ResourceAllocationGraph:

    def __init__(self):
        self.graph = nx.DiGraph()

    def add_process(self, process):
        self.graph.add_node(process, color="skyblue", type="process")

    def add_resource(self, resource):
        self.graph.add_node(resource, color="orange", type="resource")

    # Process -> Resource = Request
    def request_resource(self, process, resource):
        self.graph.add_edge(
            process,
            resource,
            type="request"
        )

    # Resource -> Process = Allocation
    def allocate_resource(self, resource, process):
        self.graph.add_edge(
            resource,
            process,
            type="allocation"
        )

    def show_graph(self):

        # =========================
        # Node Colors
        # =========================

        node_colors = [
            self.graph.nodes[n].get("color", "gray")
            for n in self.graph.nodes
        ]

        # =========================
        # Create More Space
        # =========================

        pos = nx.spring_layout(
            self.graph,
            k=3,
            iterations=100,
            seed=42
        )

        # =========================
        # Separate Request/Allocation Edges
        # =========================

        request_edges = []
        allocation_edges = []

        for u, v, data in self.graph.edges(data=True):

            if data.get("type") == "request":
                request_edges.append((u, v))

            elif data.get("type") == "allocation":
                allocation_edges.append((u, v))

        # =========================
        # Draw Nodes
        # =========================

        nx.draw_networkx_nodes(
            self.graph,
            pos,
            node_color=node_colors,
            node_size=2000
        )

        # =========================
        # Draw Labels
        # =========================

        nx.draw_networkx_labels(
            self.graph,
            pos,
            font_weight="bold"
        )

        # =========================
        # Draw Request Edges - RED
        # =========================

        nx.draw_networkx_edges(
            self.graph,
            pos,
            edgelist=request_edges,
            edge_color="red",
            arrows=True,
            arrowsize=20,
            width=2
        )

        # =========================
        # Draw Allocation Edges - GREEN
        # =========================

        nx.draw_networkx_edges(
            self.graph,
            pos,
            edgelist=allocation_edges,
            edge_color="green",
            arrows=True,
            arrowsize=20,
            width=2
        )

        # =========================
        # Legend
        # =========================

        process_legend = plt.Line2D(
            [0], [0],
            marker="o",
            color="w",
            label="Process",
            markerfacecolor="skyblue",
            markersize=12
        )

        resource_legend = plt.Line2D(
            [0], [0],
            marker="o",
            color="w",
            label="Resource",
            markerfacecolor="orange",
            markersize=12
        )

        request_legend = plt.Line2D(
            [0], [0],
            color="red",
            linewidth=2,
            label="Request"
        )

        allocation_legend = plt.Line2D(
            [0], [0],
            color="green",
            linewidth=2,
            label="Allocation"
        )

        plt.legend(
            handles=[
                process_legend,
                resource_legend,
                request_legend,
                allocation_legend
            ],
            loc="best"
        )

        plt.title("Resource Allocation Graph")

        plt.axis("off")

        plt.show()