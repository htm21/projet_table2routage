from Modules.utilis import *

import random as rd



class Network :

    def __init__(self) -> None:
        self.connections = []
        self.nodes : dict[ str or int : Node] = {}     
    
    
    def link_creation(self, node1, node2) :

        if node1.type == "Tier1" :

            if node2.type == "Tier1" :
                if Tier1.instance_counter < 10 and rd.random() > 0.75:
                    
                    poids = rd.randint(5,11)
                    self.connections.append((node1, node2, poids))
            
            if node2.type == "Tier2" :
                