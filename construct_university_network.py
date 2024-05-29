def construct_university_network(existing_network, classDictionary):
    # Function to construct the university-level network from the existing network

    # Initialize an empty dictionary to store university-level connectivity
    university_network = {}

    # Traverse the existing network
    for key in existing_network.keys():
        # Extract university information from the node
        node = classDictionary[key]
        university = node.uni

        # Check if the university already exists in the university_network
        if university not in university_network.keys():
            university_network[university] = set()

        # Add connections to the university network
        for connected_node in existing_network[key]:
            classNode = classDictionary[connected_node]
            connected_university = classNode.uni
            if connected_university != university:
                university_network[university].add(connected_university)

    return university_network


def count_sections(strings_list):
    sections_count = []
    for s in strings_list:
        sections = s.split(',')
        sections_count.append(len(sections))
    return sections_count

def create_dataframe_from_lists(column_names, list1, list2):
    data = list(zip(list1, list2))
    df = pd.DataFrame(data, columns=column_names)
    return df
