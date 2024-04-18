from platform import node
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
            
    def graph_creation(self) :

        for node1 in self.nodes :
            rd.shuffle(self.nodes)
            if node1.type == "Tier1" :
                for node2 in self.nodes :
                    
                    if node2.type == "Tier1" and node1.id != node2.id and rd.random() < 0.75 :
                        poids = rd.randint(5,10)
                        self.connections[node1].append((node2, poids))
                        self.connections[node2].append((node1, poids))
            
            elif node1.type == "Tier2" :

                nb_T1 = rd.randint(1,2)
                nb_T2 = rd.randint(2,3)
                for node2 in self.nodes :
                    i_t1 = len([node for node in self.connections[node1] if node[0].type == "Tier1"])
                    i_t2 = len([node for node in self.connections[node1] if node[0].type == "Tier2"])

                    if node2.type == "Tier1" :
                        if i_t1 < nb_T1 :
                            poids = rd.randint(10,20)
                            self.connections[node1].append((node2, poids))
                            self.connections[node2].append((node1, poids))
                    
                    if node2.type == "Tier2" :
                        if i_t2 < nb_T2 :
                            poids = rd.randint(10,20)
                            self.connections[node1].append((node2, poids))
                            self.connections[node2].append((node1, poids))
                        else : 
                            print("déjà plein")

        

                    
            
            