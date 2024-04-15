
from Modules.network import *


def main() :


    net = Network()

    net.creation_nodes()
    print(net.connections)
    print()
    print(net.nodes)


if __name__ == "__main__" :
    print("\033c")
    main()