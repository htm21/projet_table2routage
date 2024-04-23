
from Modules.network import *

import random as rd

def main() :


    net = Network()
    net.nodes_creation()
    net.graph_creation_2()
    # for key, val in (net.connections).items() :
    #     print(f" {key}      -->      {val} \n")
    # print(net.main_dfs())
    
    for node in net.connections:
        print(f"{node.type : <6} {node.id : <3} | {net.connections[node]}")
    net.graph_creation()
    net.check_doublon()

if __name__ == "__main__" :
    print("\033c")
    main()
