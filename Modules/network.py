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
        
        rd.shuffle(self.nodes)
        for node1 in self.nodes :


            if node1.type == "Tier1" :
                
                for node2 in self.nodes :
                    if node2.type == "Tier1" and node2.id != node1.id and rd.random() < 0.75 :
                        poids = rd.randint(5,11)
                        self.connections[node1].append((node2, poids))
                        self.connections[node2].append((node1, poids))

                    
            
            # if node1.type == "Tier2" :
            #     nb_t1 = 0
            #     nb_t2 = 0
            #     for node2 in self.nodes :
            #         if node2.type == "Tier1" :
            #             if nb_t1 == 0 :
            #                 self.connections[node1].append((node2, rd.randint(10,21)))
            #                 nb_t1 += 1
                  
            #             elif nb_t1 == 1 and rd.random() < 0.20 :
            #                 self.connections[node1].append((node2, rd.randint(10,21)))
            #                 nb_t1 += 1
            #         if node2.type == "Tier2" and node2.id != node1.id :
            #             if nb_t2 < 2 :
            #                 self.connections[node1].append((node2, rd.randint(10,21)))
            #                 nb_t2 += 1

            #             elif nb_t2 == 2 and rd.random() < 0.20 :
            #                 self.connections[node1].append((node2, rd.randint(10,21)))
            #                 nb_t2 += 1
    