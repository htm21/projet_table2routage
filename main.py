
from Modules.network import *


def main() :


    net = Network()             
    net.nodes_creation()
    net.graph_creation()
    # for key, val in (net.connections).items() :
    #     print(f" {key}      -->      {val} \n")
    print(net.main_dfs())


if __name__ == "__main__" :
    print("\033c")
    main()