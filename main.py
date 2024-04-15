
from Modules.network import *


def main() :


    net = Network()

    print(f" NODES BEFORE CREATION : {net.nodes}")
    net.creation_nodes()
    net.link_creation()
    print(net.connections)
   


if __name__ == "__main__" :
    print("\033c")
    main()