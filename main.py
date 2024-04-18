
from Modules.network import *


def main() :


    net = Network()
    net.creation_nodes()
    net.graph_creation()
    print(net.connections)
   


if __name__ == "__main__" :
    print("\033c")
    main()