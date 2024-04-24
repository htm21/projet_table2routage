
from Modules.network import *

import random as rd

def main() :


    net = Network()
    net.nodes_creation()
    net.connect_nodes()
    node_1 = rd.choice(net.nodes)
    print(f"TABLE DE ROUTAGE DE {node_1}  \n{net.next_hop(node_1)}")


if __name__ == "__main__" :
    print("\033c")
    main()
