# render_map.py
import matplotlib.pyplot as plt
import networkx as nx

# Try to use an emoji-capable font if available (won't crash if missing)
plt.rcParams['font.family'] = ['Segoe UI Emoji', 'DejaVu Sans', 'sans-serif']


def render_galaxy_map(galaxy, player_sector=None, save_png=False):
    """
    Safe Map Upgrade (Option A):
    - Adds gentle color-coding
    - Uses spring layout for cleaner spacing
    - Removes emoji glyphs to avoid warnings
    """

    G = nx.Graph()

    # Build graph
    for sid, sector in galaxy.sectors.items():
        # Node attributes
        G.add_node(
            sid,
            type=sector.type,
            has_port=sector.port is not None,
            has_planet=sector.planet is not None
        )

        # Edges
        for n in sector.neighbors:
            if sid < n:  # avoid duplicates
                G.add_edge(sid, n)

    # Layout (spring layout is more readable)
    pos = nx.spring_layout(G, seed=42, k=0.5)

    # Color map by sector type
    def node_color(sid):
        t = G.nodes[sid]["type"]
        if sid == player_sector:
            return "#FFD700"     # gold
        if t == "STARDOCK":
            return "#00BFFF"     # deep sky blue
        if t == "FEDSPACE":
            return "#87CEFA"     # light blue
        if t == "PIRATE":
            return "#FF6347"     # tomato red
        if t == "DEADEND":
            return "#808080"     # gray
        return "#90EE90"         # default (light green)

    colors = [node_color(sid) for sid in G.nodes()]

    # Draw edges first
    nx.draw_networkx_edges(G, pos, alpha=0.4)

    # Draw nodes
    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=colors,
        node_size=500,
        edgecolors="black"
    )

    # Labels (ID only to keep it clean)
    nx.draw_networkx_labels(G, pos, font_size=8, font_color="black")

    plt.title("TW2025 Galaxy Map")
    plt.axis("off")

    if save_png:
        plt.savefig("tw2025_map.png", dpi=200)
        print("Map saved as tw2025_map.png")

    plt.show()
