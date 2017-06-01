import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import graphviz_layout


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


# https://stackoverflow.com/questions/29586520/can-one-get-hierarchical-graphs-from-networkx-with-python-3
def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5,
                  pos=None, parent=None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = G.neighbors(root)
    if parent != None:
        neighbors.remove(parent)
    if len(neighbors) != 0:
        dx = width / len(neighbors)
        nextx = xcenter - width / 2 - dx / 2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap,
                                vert_loc=vert_loc - vert_gap, xcenter=nextx, pos=pos,
                                parent=root)
    return pos


if __name__ == '__main__':
    distribution = count_character("jnwrgpogwg wg wyabcdefhstuvxyz gwkeg"
                                   "owepg iwegiowoieg qwpgoe iwepogiweg gopweabcdefghilmnprqrstuvwxizjklm")
    print(sorted(list(distribution.items()), key=lambda x: x[1]))
    code_tree = huffman_algorithm(distribution)
    print(sorted(code_tree[1], key=lambda x: len(x[1])))
