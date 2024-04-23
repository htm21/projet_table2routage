from Modules.node import *                  # On importe les class des Nœuds créé pour pouvoir les utilisés
from itertools import combinations

import random as rd                         # On importe le module random pour générer quelque truc aléatoirement

class Network :                             # Création de la class Network

    def __init__(self) -> None: 
        self.connections : dict[Node : list] = {}               # un Network contient des connections entre Nodes (c.f Association des Nodes)
        self.nodes : list[Node] = []              # un Network contient aussi une liste de Nodes (ça serait bête sinon)
        
        self.tier1_nodes : list[Node] = []
        self.tier2_nodes : list[Node] = []
        self.tier3_nodes : list[Node] = []


    def nodes_creation(self) -> None :      # La fonction qui va créer nos Nodes de manère uniforme !!
        
        for _ in range(10) :                # On veut 10 Tier1
            node = Tier1()
            self.nodes.append(node)         # on l'ajoute à la liste des Nodes
            self.connections[node] = []     # création d'une clé pour pouvoir connaître les connections de chaque Node
            self.tier1_nodes.append(node)
        
        for _ in range(20) :                # Même logique ...
            node = Tier2()
            self.nodes.append(node)
            self.connections[node] = []
            self.tier2_nodes.append(node)
        
        for _ in range(70) :
            node = Tier3()
            self.nodes.append(node)
            self.connections[node] = []
            self.tier3_nodes.append(node)

    ######################################## CRÉATION DU GRAPHE NON ORIENTÉ DU RÉSEAU ########################################################################


    def connect_tier_1_nodes(self) -> None:
        possible_connections = int((10 * (10 - 1)) / 2)
        node_combinizations = list(combinations(self.tier1_nodes, 2))
        connections = [rd.random() < 0.75 for _ in range(possible_connections)]

        for index, connection in enumerate(connections):
            if connection:
                poids = rd.randint(5,10)
                node_1, node_2 = node_combinizations[index][0], node_combinizations[index][1]
                self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))


    def connect_tier_2_nodes(self) -> None:
        for node_1 in self.tier2_nodes:
            
            backbone_connections = rd.randint(1, 2)
            while backbone_connections != 0:
                node_2 = rd.choice(self.tier1_nodes) 
                if not any([node_2 is node for node in self.connections[node_1]]):
                    poids = rd.randint(10,20) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    backbone_connections -= 1

            transit_opertator_connections = rd.randint(2, 3)
            while transit_opertator_connections != 0:
                node_2 = rd.choice(self.tier2_nodes)
                if not any([node_2 is node for node in self.connections[node_1]]) and node_1 is not node_2:
                    poids = rd.randint(10, 20) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    transit_opertator_connections -= 1


    def connect_tier_3_nodes(self) -> None:
        for node_1 in self.tier3_nodes:
            opertator_connections = 2
            while opertator_connections != 0:
                node_2 = rd.choice(self.tier2_nodes)
                if not any([node_2 is node for node in self.connections[node_1]]):
                    poids = rd.randint(20, 50) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    opertator_connections -= 1


    def graph_creation_2(self) -> None:
        self.connect_tier_1_nodes()
        self.connect_tier_2_nodes()
        self.connect_tier_3_nodes()
         

    def graph_creation(self) -> None :
        ''' Fonction qui créer un graphe non-orienté, avec des poids en fonction des types de Noeuds'''

        rd.shuffle(self.nodes)                # On mélange le tout, (évite de toujours avoir le même type à la chaine)                  
        for node1 in self.nodes :             # C'EST PARTI 
            if node1.type == "Tier1" :        # Si le Node est de type Tier1, quelles sont les possibilités ????

                for node2 in self.nodes :     # On parcours les autres Nodes (une amitié se fait avec deux personnes)

                    if node2.type == "Tier1" and node1.id != node2.id :     # Si cet autre Noeud est un Tier1 aussi et différent, (attention schizophrène)
                        if rd.random() < 0.75 :                             # Un lien existe à 75% de chance
                            poids = rd.randint(5,10)                        # on génère un poids entre 5 et 10 (compris et aléatoire)
                            self.connections[node1].append((node2, poids))  # et on ajoute un amis à Node1 avec le poids de leur lien
                            self.connections[node2].append((node1, poids))  # de même pour le Node2, une amitié RÉCIPROQUE !!

            elif node1.type == "Tier2" :            # Si le Node est de type Tier2, what's the possibility ??

                for node2 in self.nodes :           # même logique
                    if node2.type == "Tier1" :      # Si cet autre Noeud est un Tier1, qu'est ce qu'on va faire ?
                        if node2 in self.connections[node1] :   # on va d'abord vérifier si ce Noeud n'est pas déjà présent dans les connecitons du Node
                            continue                            # si c'est le cas on skip ce Noeud (il essaie de gratter l'amitié)
                        else :
                            T1 = len([node for node in self.connections[node1] if node[0].type == "Tier1"])    # Dans l'autre cas on va d'abord compter le nombre de Tier1 connectés au Node
                            N2_T2 = len([node for node in self.connections[node2] if node[0].type == "Tier2"]) # Et le nombre de Tier2 connecter au second Noeud (évite les ajouts non-uniforme)
                            if T1 < node1.nt1 and N2_T2 < node2.nt2 :               # donc on compare les attribut des instances et les connections pour voir si une connection est dispo
                                poids = rd.randint(10,20)                           # dans ce cas là, on a un lien Tier1 <-> Tier2, donc on prend un poids entre 10 et 20 (aléatoire)
                                self.connections[node1].append((node2, poids))      # même logique
                                self.connections[node2].append((node1, poids))
                    
                    elif node2.type == "Tier2" and node2.id != node1.id :   # Si cet autre Noeud est aussi un Tier2, on vérifie si c'est pas le même
                        if node2 in self.connections[node1] :               # même logique
                            continue
                        else :
                            node1_T2 = len([node for node in self.connections[node1] if node[0].type == "Tier2"])   # on compte le nombre de Tier2 pour le Node initial
                            node2_T2 = len([node for node in self.connections[node2] if node[0].type == "Tier2"])   # de même pour le second Noeud 
                            if node1_T2 < node1.nt2 and node2_T2 < node2.nt2 :      # une amitié est dispo ?
                                poids = rd.randint(10,20)                           # Dans ce cas là même logique, lien Tier2 <-> Tier2, donc on prend un poids entre 10 et 20 
                                self.connections[node1].append((node2, poids))      # ...
                                self.connections[node2].append((node1, poids))
            

            elif node1.type == "Tier3":            # Si le Node est un Tier3, ¿ cuáles son las posibilidades ??? En réalité, il y en a qu'une seule (lien T3 <-> T2)                                      
                potential_tier2_nodes = [node for node in self.nodes if node.type == "Tier2"]   # On fait une liste de lien potentiels (que des T2)
                connected_tier2_nodes = []                                                      # et une liste qui stockera les amitiés

                
                while len(connected_tier2_nodes) < 2:       # les meilleurs groupes d'amis sont souvent les plus petit, donc ici on veut que ça soit exactement égale à 2 
                   
                    potential_tier2_nodes.sort(key=lambda x: len([node for node in self.connections[x] if node[0].type == "Tier3"]))# On trie les noeuds T2 potentiels par nombre de connexions T3 croissant
                    for node2 in potential_tier2_nodes:                                     # On parcours ces Noeuds
                        if node2 not in connected_tier2_nodes:                              # Si le Noeud n'est pas connecter au Node principale (n'est pas dans la liste)
                            if node2 not in [conn[0] for conn in self.connections[node1]]:  # On vérifie plus profondément pour être sûr de nous (perfectionnisme !)
                                poids = rd.randint(20, 50)                                  # On a donc un lien T3 <-> T2 de poids entre 20 et 50
                                self.connections[node1].append((node2, poids))              # même logique 
                                self.connections[node2].append((node1, poids))
                                connected_tier2_nodes.append(node2)                         # on ajoute le Noeud au Noeud connectés au Node principal
                                if len(connected_tier2_nodes) == 2:                         # on vérifie si on a pas une amitié parfaite
                                    break                                                   # dans ce cas là on s'arrête là pour ce Node principal

    
    def check_doublon(self) :
        for node in self.nodes :
            dejavu = []
            for element in self.connections[node] :
                if element[0] in dejavu :
                    print(f"ISSUE : {node} -> {element[0]} in {self.connections[node]} \n")
                dejavu.append(element[0])  


    ######################################## COMMENT VERIFIER SI UN GRAPH EST CONNEXE ? PARCOURS EN LARGEUR OU PROFONDEUR ########################################################################

    
    def PP(self, traiter, node) -> None :
        ''' Fonction PP qui va faire le parcours en profondeur du Noeud en entrée en le stockant et de ses voisins'''    
        if node not in traiter :                       
            traiter.append(node)                       # si le Noeud n'est pas dans la liste traiter alors on l'ajoute
            for connection in self.connections[node] : # on regard ses connections
                self.PP(traiter, connection[0])        # et on effectue à leur tour un parcours en profondeur
    
    def main_dfs(self) -> bool :
        ''' Fonction main du parcours en largeur, elle va créer la liste qui contiendra tout les noeuds atteint'''
        traiter = []                                   # inventaire des noeuds "marquer"
        depart = self.nodes[rd.randint(1,100)]         # il nous faut une racine pour démarer (on prend aléatoirement)
        self.PP(traiter, depart)                       # on lance la fonction PP récursive
        
        return len(traiter) == len(self.nodes)         # on vérifie si la longueur de la liste "traiter" est égale la taille de la liste contenant tout les nodes (self.nodes)