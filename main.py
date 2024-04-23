
from Modules.network import *

import random as rd

def main() :


    net = Network()             
    net.nodes_creation()
    net.graph_creation()
    net.check_doublon()

if __name__ == "__main__" :
    print("\033c")
    main()
