from Modules.node import *                  # On importe les class des Nœuds créé pour pouvoir les utilisés
from itertools import combinations

import heapq
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
                
                node_1.backbone_connections += 1 ; node_2.backbone_connections += 1


    def connect_tier_2_nodes(self) -> None:
        for node_1 in self.tier2_nodes:
            
            backbone_connections = rd.randint(1, 2)
            while backbone_connections != 0:
                node_2 = rd.choice(self.tier1_nodes) 
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):
                    poids = rd.randint(10,20) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    
                    node_1.backbone_connections += 1 ; node_2.backbone_connections += 1
                    backbone_connections -= 1


            transit_opertator_connections = rd.randint(2, 3)
            while transit_opertator_connections != 0:
                node_2 = rd.choice(self.tier2_nodes)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]) and node_1 is not node_2:
                    poids = rd.randint(10, 20) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    
                    node_1.transit_opertator_connections += 1 ; node_2.transit_opertator_connections += 1
                    transit_opertator_connections -= 1


    def connect_tier_3_nodes(self) -> None:
        for node_1 in self.tier3_nodes:
            opertator_connections = 2
            while opertator_connections != 0:
                node_2 = rd.choice(self.tier2_nodes)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):
                    poids = rd.randint(20, 50) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    
                    node_1.transit_opertator_connections += 1 ; node_2.opertator_connections += 1
                    opertator_connections -= 1


    def connect_nodes(self) -> None:
        self.connect_tier_1_nodes()
        self.connect_tier_2_nodes()
        self.connect_tier_3_nodes()
         


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


    def shortest_weighted_path(self, start_node, end_node):
        dist = {node : float('inf') for node in self.nodes}
        dist[start_node] = 0
        queue = [(start_node, 0)]


        while queue:
            
            # Here we take the node with the smallest distance from our start node       
            current_node, current_dist = queue.pop(min(enumerate(queue), key = lambda node_distance: node_distance[1][1])[0])
            
            if current_dist > dist[current_node]: continue
            for neighbor_node, weight in self.connections[current_node]:
                distance = current_dist + weight
                if distance < dist[neighbor_node]:
                    dist[neighbor_node] = distance
                    queue.append((neighbor_node, distance))

        path = []
        current_node = end_node
        while current_node != start_node:
            path.append(current_node)
            for neighbor_node, weight in self.connections[current_node]:
                if dist[current_node] == dist[neighbor_node] + weight:
                    current_node = neighbor_node
                    break
        path.append(start_node)
        path.reverse()
        return path
    
    def calculate_path_weight(self, path : list[Node]):
        weight = 0
        for index in range(len(path) - 1):
            for connection in self.connections[path[index]]:
                neighbouring_node = connection[0]
                if neighbouring_node is path[index + 1]:
                    weight += connection[1]
        return weight


    def next_hope(self, start_node) :
        ''' Fonction qui forme la table de routage pour le noeud en entrée, utilisation de https://www.youtube.com/watch?v=LGiRB_lByh0&t=1027s '''
        
        distance = {node : float("inf") for node in self.connections}   # comme dans djikstra, on fixe tout les noeuds à distance "infini" 
        distance[start_node] = 0                                        # alors que le node de départ "start_node" est nul

        next_hope = {node : None for node in self.connections}          # de même pour le prochain noeud, ils sont tous nuls au départ
        next_hope[start_node] = start_node                              # le prochain noeud pour atteindre le noeud de départ est lui même
        
        unvisited = set(self.connections.keys())

        while unvisited :
            current_node = min(unvisited, key= lambda node : distance[node])    # mini par rapport à leur distance, on prendra toujours start_node en premier car sa distance vaudra toujours 0
            unvisited.remove(current_node)

            for neighbor, weight in self.connections[current_node] :
                if neighbor in unvisited :                      
                    new_dist = distance[current_node] + weight  # on calcul la distance, si elle est meilleure (plus faible) => on mets à jour

                    if new_dist < distance[neighbor] :      # dans djikstra, si la val est inférieur au poids actuelle
                        distance[neighbor] = new_dist       # -> on la modifie, sinon on passe

                    if current_node == start_node :         # si connecté au noeud de départ
                        next_hope[neighbor] = neighbor      # alors le prochain noeud pour atteindre son voisin est lui même
                    else :
                        next_hope[neighbor] = next_hope[current_node]   # sinon on place comme prochain noeud, le prochain noeud du noeud actuel
                        
        return next_hope