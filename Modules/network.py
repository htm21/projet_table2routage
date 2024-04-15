from Modules.utilis import *

import random as rd



class Network :

    def __init__(self) -> None:
        self.connections = {}
        self.nodes : list = []
    
    def creation_nodes(self) :
        
        for _ in range(10) :
            node = Tier1()
            self.nodes.append(node)
            self.connections[node] = []
        
        for _ in range(20) :
            node = Tier2()
            self.nodes.append(node)
            self.connections[node] = []
        
        for _ in range(70) :
            node = Tier3()
            self.nodes.append(node)
            self.connections[node] = []
            

    
    def link_creation(self) :
        pass