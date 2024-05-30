import folium
import networkx as nx
from IPython.display import HTML

def visualisation_network(network, pos, node_labels=None, node_colors=None, node_sizes=None, edge_labels=None):
    # Create an undirected graph
    G = nx.Graph()

    # Add nodes and edges from the network dictionary
    G.add_nodes_from(network.keys())
    for node, neighbors in network.items():
        G.add_edges_from((node, neighbor) for neighbor in neighbors)

    # Create a Folium map centered at the mean latitude and longitude of nodes
    center_lat = sum(lat for lat, lon in pos.values()) / len(pos)
    center_lon = sum(lon for lat, lon in pos.values()) / len(pos)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=4)

    # Plot nodes
    for node, (lat, lon) in pos.items():
        radius = node_sizes[node] if node_sizes else 5
        color = node_colors[node] if node_colors else 'blue'
        folium.CircleMarker(location=[lat, lon], radius=radius, color=color, fill=True).add_to(m)

    # Plot edges
    for edge in G.edges():
        start_lat, start_lon = pos[edge[0]]
        end_lat, end_lon = pos[edge[1]]
        folium.PolyLine(locations=[[start_lat, start_lon], [end_lat, end_lon]], color='black').add_to(m)

    # Add node labels
    if node_labels:
        for node, (lat, lon) in pos.items():
            folium.Marker([lat, lon], popup=node_labels[node]).add_to(m)

    # Add edge labels
    if edge_labels:
        for edge, label in edge_labels.items():
            start_lat, start_lon = pos[edge[0]]
            end_lat, end_lon = pos[edge[1]]
            folium.Marker([(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], popup=label).add_to(m)

    # Return HTML representation of the map
    return m._repr_html_()
