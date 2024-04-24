
from Modules.network import *

import random as rd

def main() :


    net = Network()
    net.nodes_creation()
    net.connect_nodes()
    # for key, val in (net.connections).items() :
    #     print(f" {key}      -->      {val} \n")
    # print(net.main_dfs())
    
    # for node in net.connections:
    #     print(f"{node.type : <6} {node.id : <3} | {net.connections[node]}")
    # node_1, node_2 = rd.choice(net.tier1_nodes), rd.choice(net.tier1_nodes)
    # print(node_1, node_2)
    # path = net.shortest_weighted_path(node_1, node_2)
    # print(path)
    # print(net.calculate_path_weight(path))
    node_1 = rd.choice(net.nodes)
    print(f"NODE : {node_1} : {net.next_hope(node_1)}")


if __name__ == "__main__" :
    print("\033c")
    main()
