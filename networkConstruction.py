import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

def create_network_data_structure_from_strings(input_strings, network=None, edge_counts=None):
    if network is None:
        network = {}  # Initialize an empty graph (adjacency list representation)
    if edge_counts is None:
        edge_counts = {}  # Initialize an empty dictionary to store edge counts

    for input_string in input_strings:
        # Split the input string using semicolons while conserving everything between semicolons
        split_list = [elem.strip() for elem in input_string.split(';')]
        # Apply the algorithm to update the fully-connected network data structure
        network, edge_counts = update_fully_connected_network(split_list, network, edge_counts)

    return network, edge_counts

def update_fully_connected_network(elements, network, edge_counts):
    # Connect every pair of elements together
    for i in range(len(elements)):
        for j in range(i+1, len(elements)):
            item1 = elements[i]
            item2 = elements[j]
            # Add edge between item1 and item2
            if item1 not in network:
                network[item1] = set()
            if item2 not in network:
                network[item2] = set()
            network[item1].add(item2)
            network[item2].add(item1)  # Undirected graph, so add edges in both directions

            # Update edge count
            edge = (item1, item2)
            edge_counts[edge] = edge_counts.get(edge, 0) + 1

    return network, edge_counts

# Example usage:
# input_strings = listCollabs
# network_data_structure, edge_counts = create_network_data_structure_from_strings(input_strings)
# print("Network data structure:")
# print(network_data_structure)
# print("Edge counts:")
# print(edge_counts)

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

def analyze_network(network, subgraph_nodes=None):
    if subgraph_nodes is None:
        subgraph_nodes = network.keys()

    # Number of nodes is the number of subgraph nodes
    num_nodes = len(subgraph_nodes)

    # To count the number of edges
    num_edges = 0
    seen_edges = set()  # To avoid double counting edges in an undirected graph

    for node in subgraph_nodes:
        if node in network:
            connections = network[node]
            for connected_node in connections:
                if connected_node in subgraph_nodes:
                    # Use a frozenset to represent the edge to avoid counting the same edge twice
                    edge = frozenset([node, connected_node])
                    if edge not in seen_edges:
                        seen_edges.add(edge)
                        num_edges += 1

    return num_nodes, num_edges

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

def remove_node(network, node_to_remove):
    # Remove the node from the dictionary if it exists
    if node_to_remove in network:
        del network[node_to_remove]

    # Iterate over all remaining nodes in the network
    for key, value in network.items():
        # Remove references to the node_to_remove from adjacency lists
        if node_to_remove in value:
            value.remove(node_to_remove)

def extract_subnetwork(network, target_university):
    # Check if the target university is in the network
    if target_university not in network:
        return {}

    # Get the direct connections of the target university
    direct_connections = network[target_university]

    # Create the sub-network
    subnetwork = {target_university: direct_connections}

    # Add the connections of the direct connections
    for university in direct_connections:
        if university in network:
            subnetwork[university] = network[university]

    return subnetwork

def complete_network_fun(network):
    # Create a set to collect all nodes
    all_nodes = set(network.keys())
    for connections in network.values():
        all_nodes.update(connections)

    # Ensure all nodes are keys in the network dictionary
    for node in all_nodes:
        if node not in network:
            network[node] = []

    return network

def match_dict_values(dict1, dict2):
    matched_dict = {}

    for key in dict1.keys():
      if key in dict2.keys():
          matched_dict[key] = dict2[key]
      else:
          matched_dict[key] = None

    node_labels = {item: item for item in list(dict1)}

    return matched_dict, node_labels

def remove_nodes_from_topology(topology, nodes_to_remove):
    # Iterate over the dictionary keys (nodes) and values (neighbors)
    for node, neighbors in list(topology.items()):
        # Check if the current node is in the nodes_to_remove list
        if node in nodes_to_remove:
            # Remove the node from the dictionary
            del topology[node]
        else:
            # Remove the nodes to remove from the list of neighbors
            topology[node] = [neighbor for neighbor in neighbors if neighbor not in nodes_to_remove]
            # Remove any empty neighbor lists
            if not topology[node]:
                del topology[node]
        # Remove references to the removed nodes in the neighbor lists
        for neighbor, neighbors_of_neighbor in topology.items():
            topology[neighbor] = [n for n in neighbors_of_neighbor if n not in nodes_to_remove]

def combine_nodes(network_dict, nodes_to_combine):
    # Create a NetworkX graph from the dictionary
    G = nx.Graph()
    for node, neighbors in network_dict.items():
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    # Combine nodes
    for group in nodes_to_combine:
        new_node = next(iter(group)).upper()  
                                      # Name the new node by concatenating old node names
                                      # for this to work the new_node needs a new name
                                      # otherwise when the algorithm checks if its already in
                                      # the network it will return true
        for node in group:
            if node in G:
                # Add edges from the new node to the neighbors of the old nodes
                for neighbor in list(G.neighbors(node)):
                    if neighbor not in group:
                        G.add_edge(new_node, neighbor)
                G.remove_node(node)  # Remove the old node

    # Convert back to dictionary format
    new_network_dict = {node: list(G.neighbors(node)) for node in G.nodes()}

    return new_network_dict

def lowercase_dict(input_dict):
    def lowercase_value(value):
        if isinstance(value, str):
            return value.lower()
        elif isinstance(value, list):
            return [lowercase_value(item) for item in value]
        else:
            return value

    return {key.lower(): lowercase_value(value) for key, value in input_dict.items()}
