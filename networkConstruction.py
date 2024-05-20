def search_nodes(network, keyword):
    matches = []
    for node, neighbors in network.items():
        if keyword.lower() in node.lower():
            matches.append((node, len(neighbors), neighbors))

    matches.sort(key=lambda x: x[1], reverse=True)  # Sort matches by number of connections (descending)
    return matches

def print_search_results(search_results):
    print("Search Results:")
    for match in search_results:
        node, num_connections, neighbors = match
        print(f"Node: {node} | Number of Connections: {num_connections}")
        print("Neighbors:", neighbors)
        print()

# Example usage:
# keyword_to_search = "ucl"  # Example keyword to search
# search_results = search_nodes(filtered_network, keyword_to_search)
# print_search_results(search_results)

import matplotlib.pyplot as plt
import networkx as nx

def plot_network_for_nodes_with_connections(network, num_connections):
    # Create a NetworkX graph from the network dictionary
    G = nx.Graph(network)

    # Filter nodes based on the number of connections
    nodes_with_given_connections = [node for node in G.nodes() if G.degree(node) == num_connections]

    # Create a subgraph containing only the filtered nodes
    subgraph = G.subgraph(nodes_with_given_connections)

    # Plot the subgraph
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(subgraph, k=0.3)  # Adjust 'k' to increase or decrease spacing between nodes

    #pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=False, node_color='skyblue', node_size=3, edge_color='gray', linewidths=10)
    plt.title(f"Network for nodes with {num_connections} connections")
    plt.show()

    # Print nodes in tabulated form with wider display width
    pd.set_option('display.width', 1000)  # Set display width to prevent text from being cut off
    nodes_table = pd.DataFrame({'Node': nodes_with_given_connections})
    print(f"\nNodes with {num_connections} connections:")
    print(nodes_table)

# Example usage:
# num_connections_to_plot = 11
# plot_network_for_nodes_with_connections(filtered_network, num_connections_to_plot)

def nodes_with_connections(network, num_connections):
    nodes = []
    for node, neighbors in network.items():
        if len(neighbors) == num_connections:
            nodes.append(node)
    return nodes

def print_nodes_with_connections(nodes, num_connections):
    print(f"Nodes with {num_connections} connections:")
    print(nodes)

# Example usage:
# Investigate nodes with a specific number of connections
# num_connections_to_investigate = 11
# nodes_with_given_connections = nodes_with_connections(network_data_structure, num_connections_to_investigate)

# Print the nodes
# print_nodes_with_connections(nodes_with_given_connections, num_connections_to_investigate)

def check_duplicate_nodes(network):
    node_names = set()
    duplicate_nodes = set()
    for node in network:
        if node in node_names:
            duplicate_nodes.add(node)
        else:
            node_names.add(node)
    return duplicate_nodes

# Example usage:
# duplicate_nodes = check_duplicate_nodes(filtered_network)

def connection_breakdown(network):
    connection_counts = {}
    for node, neighbors in network.items():
        num_connections = len(neighbors)
        connection_counts[num_connections] = connection_counts.get(num_connections, 0) + 1
    return connection_counts

# Example usage:
def print_connection_breakdown(connection_counts):
    print("Connection breakdown:")
    for num_connections, count in sorted(connection_counts.items()):
        print(f"{num_connections} connections: {count} nodes")

# Calculate connection breakdown
# connection_counts = connection_breakdown(filtered_network)

# Print the breakdown
# print_connection_breakdown(connection_counts)

def inspect_network(network):
    num_nodes = len(network)
    num_edges = sum(len(neighbors) for neighbors in network.values()) // 2  # Divide by 2 for undirected graph
    return num_nodes, num_edges

# Example usage:
# num_nodes, num_edges = inspect_network(network_data_structure)
# print("Number of nodes:", num_nodes)
# print("Number of edges:", num_edges)

def plot_clustered_network(network):
    G = nx.Graph(network)

    # Detect communities using Girvan-Newman algorithm
    communities_generator = nx.algorithms.community.girvan_newman(G)
    top_level_communities = next(communities_generator)
    next_level_communities = next(communities_generator)
    community_map = {node: i for i, nodes in enumerate(next_level_communities) for node in nodes}

    # Plot the network with nodes colored by community
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=0.15)
    cmap = plt.cm.get_cmap("tab10", len(set(community_map.values())))
    node_colors = [community_map[node] for node in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, cmap=cmap, node_size=100, with_labels=False)

    # Create a fake image for colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(node_colors), vmax=max(node_colors)))
    sm.set_array([])
    plt.colorbar(sm, label='Community')

    plt.title("Clustered Network")
    plt.show()

# Example usage:
# plot_clustered_network(filtered_network)

def visualize_network(network):
    G = nx.Graph()
    for node, neighbors in network.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, k=0.5)  # Adjust 'k' to increase or decrease spacing between nodes

    nx.draw(G, pos, with_labels=False, node_color='skyblue', node_size=100, edge_color='gray', linewidths=0.5)
    plt.title("Simplified Network Visualization")
    plt.show()


# Example usage:
# visualize_network(filtered_network)

def filter_network_by_keyword(network, edge_counts, keyword):
    filtered_nodes = [node for node in network if keyword.lower() in node.lower()]
    filtered_network = {node: [neighbor for neighbor in neighbors if keyword.lower() in neighbor.lower()]
                        for node, neighbors in network.items() if keyword.lower() in node.lower()}

    # Recount edge counts based on the filtered network
    filtered_edge_counts = {(node1, node2): count for (node1, node2), count in edge_counts.items()
                            if node1 in filtered_nodes and node2 in filtered_nodes}

    return filtered_network, filtered_edge_counts

# Example usage:
# keyword = "United Kingdom" # this is why filtered network was used since it only deals with institutions within the UK
# filtered_network, filtered_edge_counts = filter_network_by_keyword(network_data_structure, edge_counts, keyword)

# print("Filtered Network:")
# print(filtered_network)
# print("\nFiltered Edge Counts:")
# print(filtered_edge_counts)


