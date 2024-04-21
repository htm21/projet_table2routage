
from Modules.network import *

import random as rd

def main() :


    net = Network()             
    net.nodes_creation()
    net.graph_creation()
    # for key, val in (net.connections).items() :
    #     print(f" {key}      -->      {val} \n")
    # print(net.main_dfs())
    print(net.connections)

if __name__ == "__main__" :
    print("\033c")
    main()
