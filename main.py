
from Modules.network import *


def main() :


    net = Network()
    net.creation_nodes()
    net.graph_creation()
    for key, val in (net.connections).items() :
        print(f" {key}      :      {val} \n")
   


if __name__ == "__main__" :
    print("\033c")
    main()