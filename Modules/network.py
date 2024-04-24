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


    def nodes_creation(self) -> None :      
        ''' Fonction qui va initialiser l'ensemble de noeuds qui seront utilisés dans notre graphe, et nos fonctions '''
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


    #########################################################################################################################################################
    ######################################## CRÉATION DU GRAPHE NON ORIENTÉ DU RÉSEAU ########################################################################
    #########################################################################################################################################################


    def connect_tier_1_nodes(self) -> None:
        ''' Fonction qui gère les connections des Tier1 '''

        possible_connections = int((10 * (10 - 1)) / 2)
        node_combinizations = list(combinations(self.tier1_nodes, 2))
        connections = [rd.random() < 0.75 for _ in range(possible_connections)]         # connections possibles T1-T1 avec une probabilité de 75%

        for index, connection in enumerate(connections):                             
            if connection:
                poids = rd.randint(5,10)
                node_1, node_2 = node_combinizations[index][0], node_combinizations[index][1]
                self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                
                node_1.backbone_connections += 1 ; node_2.backbone_connections += 1


    def connect_tier_2_nodes(self) -> None:
        ''' Fonction qui gère les connections des Tier2 '''

        for node_1 in self.tier2_nodes:                         # on parcours les Tier2
            
            backbone_connections = rd.randint(1, 2)             # on génère un nombre aléatoire de lien possible avec des Tier1 (1 ou 2)
            while backbone_connections != 0:                    # Tant que d'une connection est possible
                node_2 = rd.choice(self.tier1_nodes)            # choix aléatoire d'un T1
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):   # vérification de lien déjà existant ; si c'est le cas, on relance la procédure
                    poids = rd.randint(10,20)                   # on genère un poids entre 10 et 2O (poids de lien T2-T2)
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))  # on ajoute les liens des deux sens (non-orienté)  
                    
                    node_1.backbone_connections += 1 ; node_2.backbone_connections += 1     # MAJ des connections
                    backbone_connections -= 1                   # réduction du nombre de connection aux Tier1 possible


            transit_opertator_connections = rd.randint(2, 3)    # Même logique pour les liens T2-T2
            while transit_opertator_connections != 0:
                node_2 = rd.choice(self.tier2_nodes)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]) and node_1 is not node_2:
                    poids = rd.randint(10, 20) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    
                    node_1.transit_opertator_connections += 1 ; node_2.transit_opertator_connections += 1
                    transit_opertator_connections -= 1


    def connect_tier_3_nodes(self) -> None:
        ''' Fonction qui gère les connections des Tier3 '''

        for node_1 in self.tier3_nodes:                 # on parcours les Tier3
            opertator_connections = 2                   # chaque Tier3 a 2 connections disponibles 
            while opertator_connections != 0:           # tant qu'on peut connecter
                node_2 = rd.choice(self.tier2_nodes)    # on choisi des Tier2 aléatoires (Rappel T3 <-> T2 seulement)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):     # on vérifie si le Tier2 n'est pas déjà lié au Tier3
                    poids = rd.randint(20, 50)                                                        # dans ce cas là -> génération d'un poids aléatoire entre 20 et 50
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))  # on ajoute les liens des deux sens (non-orienté)
                    
                    node_1.transit_opertator_connections += 1 ; node_2.opertator_connections += 1     # MAJ des connections 
                    opertator_connections -= 1          # réduction du nombre de connection aux Tier2 possible


    def connect_nodes(self) -> None:
        ''' Fonction qui rassemble les création de liens inter-noeuds '''

        self.connect_tier_1_nodes()        
        self.connect_tier_2_nodes()
        self.connect_tier_3_nodes()
    

    ##############################################################################################################################################################################
    ######################################## COMMENT VERIFIER SI UN GRAPH EST CONNEXE ? GRÂCE AUX PARCOURS ########################################################################
    ##############################################################################################################################################################################
    

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


##############################################################################################################################################################################
####################################################### TABLES DE ROUTAGE ---> NEXT HOP ######################################################################################
##############################################################################################################################################################################


    def next_hop(self, start_node) :
        ''' Fonction qui forme la table de routage pour le noeud en entrée, utilisation de https://www.youtube.com/watch?v=LGiRB_lByh0&t=1027s '''
        
        distance = {node : float("inf") for node in self.connections}           # comme dans djikstra, on fixe tout les noeuds à distance "infini" 
        distance[start_node] = 0                                                # alors que le node de départ "start_node" est nul

        next_hope = {node : None for node in self.connections}                  # de même pour le prochain noeud, ils sont tous nuls au départ
        next_hope[start_node] = start_node                                      # le prochain noeud pour atteindre le noeud de départ est lui même
        
        unvisited = set(self.connections.keys())

        while unvisited :
            current_node = min(unvisited, key= lambda node : distance[node])    # mini par rapport à leur distance, on prendra toujours start_node en premier car sa distance vaudra toujours 0
            unvisited.remove(current_node)

            for neighbor, weight in self.connections[current_node] :
                if neighbor in unvisited :                      
                    new_dist = distance[current_node] + weight                  # on calcul la distance, si elle est meilleure (plus faible) => on mets à jour

                    if new_dist < distance[neighbor] :                          # dans djikstra, si la val est inférieur au poids actuelle
                        distance[neighbor] = new_dist                           # -> on la modifie, sinon on passe

                    if current_node == start_node :                             # si connecté au noeud de départ
                        next_hope[neighbor] = neighbor                          # alors le prochain noeud pour atteindre son voisin est lui même
                    else :
                        next_hope[neighbor] = next_hope[current_node]           # sinon on place comme prochain noeud, le prochain noeud du noeud actuel
                        
        return next_hope                                                        # on renvoie la table de routage du start_node