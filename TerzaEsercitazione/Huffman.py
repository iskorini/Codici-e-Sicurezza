import networkx as nx


def huffman_algorithm(character_distribution):
    distribution_list = list(character_distribution.items())
    binary_tree_code = nx.DiGraph()
    for node in distribution_list:
        binary_tree_code.add_node(node[0], freq=node[1], used=0, is_char=1)
    while (len(list(filter(lambda x: x[1]["used"] == 0, binary_tree_code.nodes(data=True))))) > 1:
        not_used_nodes = list(filter(lambda x: x[1]["used"] == 0, binary_tree_code.nodes(data=True)))
        first_node = min(not_used_nodes, key=lambda x: x[1]["freq"])
        not_used_nodes.remove(first_node)
        second_node = min(not_used_nodes, key=lambda x: x[1]["freq"])
        not_used_nodes.remove(second_node)
        binary_tree_code.node[first_node[0]]["used"] = 1
        binary_tree_code.node[second_node[0]]["used"] = 1
        binary_tree_code.add_node(first_node[0] + second_node[0],
                                  freq=first_node[1]["freq"] + second_node[1]["freq"], used=0, is_char=0)
        binary_tree_code.add_edge(first_node[0] + second_node[0], first_node[0], code=0)
        binary_tree_code.add_edge(first_node[0] + second_node[0], second_node[0], code=1)
    root = list(filter(lambda x: x[1]["used"] == 0, binary_tree_code.nodes(data=True)))
    single_character_nodes = list(filter(lambda x: x[1]["is_char"] == 1, binary_tree_code.nodes(data=True)))
    paths = []
    codes = []
    for node in single_character_nodes:
        paths.append(nx.dijkstra_path(binary_tree_code, root[0][0], node[0][0]))
    for path in paths:
        code = ""
        for i in range(0, len(path) - 1):
            code = code + str(binary_tree_code.get_edge_data(path[i], path[i + 1])["code"])
        codes.append((path[-1], code))
    return binary_tree_code, codes, root[0]


def count_character(text):
    text_no_space = text.replace(" ", "")
    occurences = dict()
    for character in list(map(chr, range(97, 123))):
        occurences[character] = text_no_space.count(character)
    return occurences


if __name__ == '__main__':
    distribution = count_character("jnwrgpogwg wg wyabcdefhstuvxyz gwkeg"
                                   "owepg iwegiowoieg qwpgoe iwepogiweg gopweabcdefghilmnprqrstuvwxizjklm")
    print(sorted(list(distribution.items()), key=lambda x: x[1]))
    code_tree = huffman_algorithm(distribution)
    print(sorted(code_tree[1], key=lambda x: len(x[1])))
