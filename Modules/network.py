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

        rd.shuffle(self.nodes)
        for node1 in self.nodes :
            if node1.type == "Tier1" :

                for node2 in self.nodes :    
                    if node2.type == "Tier1" and node1.id != node2.id and rd.random() < 0.75 :
                        poids = rd.randint(5,10)
                        self.connections[node1].append((node2, poids))
                        self.connections[node2].append((node1, poids))

            elif node1.type == "Tier2" :
                nb_t1 = rd.randint(1,2)
                nb_t2 = rd.randint(2,3)

                for node2 in self.nodes :
                    if node2.type == "Tier1" :
                        if node2 in self.connections[node1] : 
                            continue
                        else :
                            T1 = len([node for node in self.connections[node1] if node[0].type == "Tier1"])
                            if T1 < nb_t1 :
                                poids = rd.randint(10,20)
                                self.connections[node1].append((node2, poids))
                                self.connections[node2].append((node1, poids))
                    
                    elif node2.type == "Tier2" and node2.id != node1.id :
                        if node2 in self.connections[node1] : 
                            continue
                        else :
                            T2 = len([node for node in self.connections[node1] if node[0].type == "Tier2"])
                            if T2 < nb_t2 :
                                poids = rd.randint(10,20)
                                self.connections[node1].append((node2, poids))
                                self.connections[node2].append((node1, poids))



            
            

        

                    
            
            