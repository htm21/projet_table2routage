from Modules.custom_button import *
from Modules.utils import *
from Modules.node import *                  # On importe les class des Nœuds créé pour pouvoir les utilisés
from itertools import combinations          # On importe la fonction combinations de itertools pour faciliter la formation de liens (cf connect_tier_1_nodes())
from time import time

import tkinter as tk                        # On importe le module tkinter pour la mise en place de l'interface graphique de notre application
import random as rd                         # On importe le module random pour générer quelque truc aléatoirement



class Network(tk.Canvas):                             # Création de la class Network

    def __init__(self, parent : tk.Widget, app : object, *args : tuple, **kwargs : dict) -> None: 
        
        # GUI Stuff ====================================================================

        tk.Canvas.__init__(self, parent, *args, **kwargs)
        self.app = app
        self.parent : tk.Frame = parent
        self.kwargs = kwargs
        self.canvas_id_to_node : dict[int : Node] = {}
        self.icons = {
            "Network" : (load_to_size("network", 100, 100), load_to_size("highlight_network", 100, 100)),
            "Backbone" : (load_to_size("backbone_node", 80, 80), load_to_size("highlight_backbone_node", 80, 80)),
            "TransitOperator" : (load_to_size("transit_operator_node", 60, 60), load_to_size("highlight_transit_operator_node", 60, 60)),
            "Operator" : (load_to_size("operator_node", 30, 30), load_to_size("highlight_operator_node", 30, 30)),
            }

        self.selected_node : Node = None
        self.bind("<Button-1>", self.select_object)

        self.create_network_button = CustomButton(parent = self, parent_obj = self, func_arg = "create_network", icons = self.icons["Network"], image = self.icons["Network"][0], compound = "top", text = "Create\nNetwork", justify = "center", font = f"{font} 28 bold", foreground = "#FFFFFF", background = self.kwargs["background"])
        self.create_network_button.place(anchor = "center", relx = 0.5, rely = 0.5)


        
        # Logic Stuff ==================================================================

        self.connections : dict[Node : list[Node]] = {}               # un Network contient des connections entre Nodes (c.f Association des Nodes)
        self.nodes : list[Node] = []              # un Network contient aussi une liste de Nodes (ça serait bête sinon)
        
        self.tier1_nodes : list[Node] = []                      # création d'une liste qui contiendra les Tier1
        self.tier2_nodes : list[Node] = []                      # ... Tier2
        self.tier3_nodes : list[Node] = []                      # ... Tier3


    #########################################################################################################################################################
    ######################################## INITIALISATION DES NŒUDS PRÉSENTS DANS LE RÉSEAU ###############################################################
    #########################################################################################################################################################

    def nodes_creation(self) -> None :      # La fonction qui va créer nos Nodes de manère uniforme !!
        ''' Fonction qui va initialiser nos Tier de manière uniforme, en initialisant également leur liste de connections, etc. '''
        
        boundries = set_node_boundries(self.winfo_width() // 2, (self.winfo_height() // 2) - 50)
        bb_ovrlp = 45 if platform.system() == "Windows" else 25
        top_ovrlp = 35 if platform.system() == "Windows" else 15
        op_ovrlp = 20 if platform.system() == "Windows" else 10

        for _ in range(10) :                                # On veut 10 Tier1
            x, y = choose_coords(boundries, "Backbone")
            overlap = self.find_overlapping(x - bb_ovrlp, y - bb_ovrlp, x + bb_ovrlp, y + bb_ovrlp)
            while overlap:
                x, y = choose_coords(boundries, "Backbone")
                overlap = self.find_overlapping(x - bb_ovrlp, y - bb_ovrlp, x + bb_ovrlp, y + bb_ovrlp)

            canvas_id = self.create_image(x, y, image = self.icons["Backbone"][0], tags = ["node", "obj"])          
            node = Tier1(canvas_id = canvas_id)             # initialisation du Node
    
            self.nodes.append(node)                         # on l'ajoute à la liste des Nodes
            self.connections[node] = []                     # création d'une clé pour pouvoir connaître les connections de chaque Node
            self.tier1_nodes.append(node)                   # on ajoute le Node à la liste des Tier1 (permettra de s'organiser lors des connections inter node)
            self.canvas_id_to_node[canvas_id] = node
        

        for _ in range(20) :                                # On veut 20 Tier2
            x, y = choose_coords(boundries, "TransitOperator")
            overlap = self.find_overlapping(x - top_ovrlp, y - top_ovrlp, x + top_ovrlp, y + top_ovrlp)
            while overlap:
                x, y = choose_coords(boundries, "TransitOperator")
                overlap = self.find_overlapping(x - top_ovrlp, y - top_ovrlp, x + top_ovrlp, y + top_ovrlp)

            canvas_id = self.create_image(x, y, image = self.icons["TransitOperator"][0], tags = ["node", "obj"])
            node = Tier2(canvas_id = canvas_id)             # initialisation du Node
            
            self.nodes.append(node)                         # on l'ajoute à la liste des Nodes
            self.connections[node] = []                     # création d'une clé pour pouvoir connaître les connections de chaque Node
            self.tier2_nodes.append(node)                   # on ajoute le Node à la liste des Tier1 (permettra de s'organiser lors des connections inter node)
            self.canvas_id_to_node[canvas_id] = node
        

        for _ in range(70) :                                # On veut 70 Tier3
            x, y = choose_coords(boundries, "Operator")
            overlap = self.find_overlapping(x - op_ovrlp, y - op_ovrlp, x + op_ovrlp, y + op_ovrlp)
            while overlap:
                x, y = choose_coords(boundries, "Operator")
                overlap = self.find_overlapping(x - op_ovrlp, y - op_ovrlp, x + op_ovrlp, y + op_ovrlp)
            
            canvas_id = self.create_image(x, y, image = self.icons["Operator"][0], tags = ["node", "obj"])
            node = Tier3(canvas_id = canvas_id)             # initialisation du Node
            
            self.nodes.append(node)                         # on l'ajoute à la liste des Nodes
            self.connections[node] = []                     # création d'une clé pour pouvoir connaître les connections de chaque Node
            self.tier3_nodes.append(node)                   # on ajoute le Node à la liste des Tier1 (permettra de s'organiser lors des connections inter node)
            self.canvas_id_to_node[canvas_id] = node


    #########################################################################################################################################################
    ######################################## CRÉATION DU GRAPHE NON ORIENTÉ DU RÉSEAU #######################################################################
    #########################################################################################################################################################

    def connect_nodes(self) -> None:
        ''' 
        Fonction qui créer le graphe non orienté contenant les 3 types de Tier, avec des liens pondérés 
        '''
        self.connect_tier_1_nodes()                         # création des liens des T1                                                   
        self.connect_tier_2_nodes()                         # création des liens des T2
        self.connect_tier_3_nodes()                         # création des liens des T3

        self.tag_raise("TransitOperator")
        self.tag_raise("Backbone")
        self.tag_raise("node")

    
    def connect_tier_1_nodes(self) -> None:
        ''' 
        Fonction qui gère les connections des Tier1 
        '''
        possible_connections = int((10 * (10 - 1)) / 2) # (n * (n - 1)) / 2 = numero de conections possibles
        node_combinizations = list(combinations(self.tier1_nodes, 2))
        connections = [rd.random() < 0.75 for _ in range(possible_connections)]         # connections possibles T1-T1 avec une probabilité de 75%

        for index, connection in enumerate(connections):                             
            if connection:
                poids = rd.randint(5, 10)
                node_1, node_2 = node_combinizations[index][0], node_combinizations[index][1]
                self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                
                self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 3, fill = "#2A2226", smooth = True, tags = ["connection", "Backbone", f"{node_1.name}", f"{node_2.name}", "obj"])

        for node in self.tier1_nodes:
            node.backbone_connections += len(self.connections[node])


    def connect_tier_2_nodes(self) -> None:
        ''' 
        Fonction qui gère les connections des Tier2 
        '''

        for node_1 in self.tier2_nodes:                         # on parcours les Tier2
            
            backbone_connections = rd.randint(1, 2)             # on génère un nombre aléatoire de connections aux Tier1 (1 ou 2)
            while backbone_connections != 0:                    # on boucle tant qu'une connection est disponible 
                node_2 = rd.choice(self.tier1_nodes)            # on prends un Tier1 aléatoirement (grâce à rd.choice() dans la liste)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):                       # si aucune connection entre les deux nœuds est active 
                    poids = rd.randint(10, 20)                                                                          # génère un poids entre 10 et 20 (car implique un Tier2)
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))  # on ajoute la connections dans les deux nœuds     
                    
                    backbone_connections -= 1
                    node_1.backbone_connections += 1; node_2.transit_opertator_connections += 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 3, fill = "#1E2422", smooth = True, tags = ["connection", "TransitOperator", f"{node_1.name}", f"{node_2.name}", "obj"])
            
            transit_opertator_connections = rd.randint(2, 3) - node_1.transit_opertator_connections   # Même logique pour les liens T2-T2

            fill_tracker : dict[Node : int] = {}

            while transit_opertator_connections > 0:
                
                node_2 = rd.choice(self.tier2_nodes)            # on choisi un Tier2 aléatoirement 
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]) and node_1 is not node_2 and node_2.transit_opertator_connections <= 2:  # Même logique
                    poids = rd.randint(10, 20)                                                                              # ...
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))      
                    
                    transit_opertator_connections -= 1
                    node_1.transit_opertator_connections += 1; node_2.transit_opertator_connections += 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 3, fill = "#1E2422", smooth = True, tags = ["connection", "TransitOperator", f"{node_1.name}", f"{node_2.name}", "obj"])
                fill_tracker[node_2] = node_2.transit_opertator_connections
                if len(fill_tracker) == len(self.tier2_nodes):
                    break


    def connect_tier_3_nodes(self) -> None:
        ''' 
        Fonction qui gère les connections des Tier3 
        '''

        for node_1 in self.tier3_nodes:                 # on parcours les Tier3
            opertator_connections = 2                   # chaque Tier3 a 2 connections disponibles 
            while opertator_connections != 0:           # tant qu'on peut connecter
                node_2 = rd.choice(self.tier2_nodes)    # on choisi des Tier2 aléatoires (Rappel T3 <-> T2 seulement)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):     # on vérifie si le Tier2 n'est pas déjà lié au Tier3
                    poids = rd.randint(20, 50)                                                        # dans ce cas là -> génération d'un poids aléatoire entre 20 et 50
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))  # on ajoute les liens des deux sens (non-orienté)

                    opertator_connections -= 1
                    node_1.transit_opertator_connections += 1; node_2.opertator_connections += 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 3, fill = "#232A22", smooth = True, tags = ["connection", "Operator", f"{node_1.name}", f"{node_2.name}", "obj"])


##############################################################################################################################################################################
######################################## COMMENT VERIFIER SI UN GRAPH EST CONNEXE ? GRÂCE AUX PARCOURS #######################################################################
##############################################################################################################################################################################
    

    def PP(self, traiter, node) -> None :
        ''' 
        Fonction PP qui va faire le parcours en profondeur du Noeud en entrée et de ses voisins en les stockant 
        '''    
        if node not in traiter :                       
            traiter.append(node)                       # si le Noeud n'est pas dans la liste traiter alors on l'ajoute
            for connection in self.connections[node] : # on regard ses connections
                self.PP(traiter, connection[0])        # et on effectue à leur tour un parcours en profondeur
    
    def main_dfs(self) -> bool :
        ''' 
        Fonction main du parcours en largeur, elle va créer la liste qui contiendra tout les noeuds atteint 
        '''
        traiter = []                                   # inventaire des noeuds "marquer"
        depart = self.nodes[rd.randint(1,100)]         # il nous faut une racine pour démarer (on prend aléatoirement)
        self.PP(traiter, depart)                       # on lance la fonction PP récursive
        
        return len(traiter) == len(self.nodes)         # on vérifie si la longueur de la liste "traiter" est égale la taille de la liste contenant tout les nodes (self.nodes)


##############################################################################################################################################################################
############################################################ C'EST PARTI POUR LES TABLES DE ROUTAGE ? ########################################################################
##############################################################################################################################################################################


    def create_routing_tables(self):
        '''
        Fonction qui calcul les tables de routage pour chaque nœud du Network
        '''

        # On parcourt tout les nœuds présents dans le réseau
        for start_node in self.nodes:
            index = 0                   # Initialiser l'index pour parcourir les nœuds destinataires

            # Continuer tant que la table de routage n'est pas complète pour le nœud de départ
            while len(start_node.routing_table) != len(self.nodes) - 1:
                end_node : Node = self.nodes[index]     # Sélection du nœud de destination
                

                # Vérifier si le nœud de destination n'est pas déjà dans la table de routage du nœud de départ
                if not start_node.routing_table.get(end_node):
                    # Calculer le plus court chemin du nœud de départ (start_node) au nœud de destination (end_node) (voir ci-dessous)
                    path = self.shortest_weighted_path(start_node, end_node)
                    
                    for index_main_node in range(len(path)):                    # on parcourt les indice de la liste path
                        main_node : Node = path[index_main_node]                # on sélectionne un node principal
                        for index_sub_node in range(len(path)):                 # même logique
                            sub_node : Node = path[index_sub_node]              # on sélectionne un sous noeud à cet indice

                            # on vérifie que c'est pas le même et dans quelle direction selectionné le nœud en fonction de sa position dans le chemin
                            if not main_node == sub_node:                       
                                index_direction = 1 if index_main_node < index_sub_node else -1                 
                                main_node.routing_table[sub_node] = path[index_main_node + index_direction]     
                
                index += 1          # passage au nœud suivant


##############################################################################################################################################################################
############################################################ POUR FINIR, PLUS COURT CHEMIN ! #################################################################################
##############################################################################################################################################################################



    def shortest_weighted_path(self, start_node, end_node) -> list[Node]:
        '''
        Fonction qui retourne le plus court chemin entre deux nœuds choisis, en utilisant l'algo de Dijkstra
        '''

        # Initialisation de la table des distances avec infini pour tous les nœuds sauf le nœud de départ
        dist = {node : float('inf') for node in self.nodes}      
        dist[start_node] = 0      
        
        # Création d'une file de priorité contenant le nœud de départ et sa distance (initialement 0)
        queue = [(start_node, 0)]                            


        while queue:

            # Sélection et suppression du nœud ayant la distance minimale dans la file       
            current_node, current_dist = queue.pop(min(enumerate(queue), key = lambda node_distance: node_distance[1][1])[0])

            # Si la distance actuelle est plus grande que la distance enregistrée, ignorer cette itération
            if current_dist > dist[current_node]: continue

            # Exploration des voisins et mise à jour des distances
            for neighbor_node, weight in self.connections[current_node]:
                distance = current_dist + weight
                if distance < dist[neighbor_node]:                                      
                    dist[neighbor_node] = distance
                    queue.append((neighbor_node, distance))

        # Reconstruction du chemin à partir du nœud d'arrivée
        path = []
        current_node = end_node
        
        while current_node != start_node:
            path.append(current_node)
            
            for neighbor_node, weight in self.connections[current_node]:
                # Trouver le nœud précédent en suivant le chemin des distances minimales enregistrées
                if dist[current_node] == dist[neighbor_node] + weight:
                    current_node = neighbor_node
                    break
        
        # Ajout du nœud de départ et inversion de la liste pour obtenir le chemin dans le bon ordre
        path.append(start_node); path.reverse()
        return path



    def reconstruct_path(self, start : Node, end : Node) -> list[Node]: 
        '''
        Fonction qui reconstruit le plus court chemin entre deux nœuds grâce au tables de routage des nœuds 
        '''
        path, node, pointer = [start], start, end             # on initialise le chemin au nœud de départ, le nœud actuel et le pointeur qui représente le nœud

        while node is not end:                                # Tant que le nœud actuel n'est pas le destination
            node = node.routing_table[pointer]                # On MAJ le node actuelle par le node qui pointe vers la destination finale (dans la table de routage du node actuel)
            path.append(node)                                 # on l'ajoute au chemin 
        
        return path                                           # on retourne le chemin 


    def calc_path_weight(self, path : list[Node]) -> int:
        '''
        Fonction qui va retourner le poids total du plus court chemin généré entre deux nodes
        '''
        weight = 0                                      # Poids nul de base 

        for index_node in range(len(path) - 1):         # on parcours tous les indices de la liste du chemin

            # On récupère les liens 2 à 2 pour obtenir le poids
            main_node : Node = path[index_node]         
            next_node : Node = path[index_node + 1]

            # On ajoute le poids si celui ci correspond au node voulu
            for connection in self.connections[main_node]:
                sub_node : Node = connection[0]
                if sub_node == next_node:
                    weight += connection[1]         # C'est ce qu'on fait ici

        return weight                               # on retourne le poids du chemin




    # GUI Functions ====================================================================



    def select_object(self, event : tk.Event):
        '''
        Fonction qui gère la mise en évidence d'un nœud lorsqu'il est sélectionné par l'utilisateur (surbrillance des bords)
        '''
        object_ids = self.find_overlapping(event.x, event.y, event.x, event.y) # Finds canvas item closest to cursor      
        
        if not object_ids: 
            self.deselect_object()
            self.app.info_panel.set_object_info(self)
            return


        if self.selected_node or self.find_withtag("highlight_path"): 
            self.deselect_object()
        

        if not "node" in self.gettags(object_ids[-1]): 
            self.deselect_object()
            self.app.info_panel.set_object_info(self)
            return

        node = self.canvas_id_to_node[object_ids[-1]]
        self.selected_node = node
        self.app.info_panel.set_object_info(node)
        line_ids = self.find_withtag(node.name)
        for line_id in line_ids:
            self.itemconfig(line_id, fill = "#FFCC22")

        self.itemconfig(node.canvas_id, image = self.icons[node.type][1])
        self.addtag_withtag("selected", node.canvas_id)


    def deselect_object(self) -> None:
        '''
        Fonction qui gère la mise en évidence d'un nœud lorsqu'il n'est pas sélectionner
        '''
        if self.selected_node:
            self.itemconfig(self.selected_node.canvas_id, image = self.icons[self.selected_node.type][0])
        
            line_ids = self.find_withtag(self.selected_node.name)
            for line_id in line_ids:
                if self.selected_node.type == "Backbone":
                    self.itemconfig(line_id, fill = "#2A2226")
                elif self.selected_node.type == "TransitOperator":
                    self.itemconfig(line_id, fill = "#1E2422")
                elif self.selected_node.type == "Operator":
                    self.itemconfig(line_id, fill = "#232A22")
        
        self.selected_node = None
        self.dtag("selected")

        if ids := self.find_withtag("highlight_path"):
            for canvas_id in ids:
                obj_tags = self.gettags(canvas_id)
                
                if "node" in obj_tags:
                    node : Node = self.canvas_id_to_node[canvas_id]
                    self.itemconfig(node.canvas_id, image = self.icons[node.type][0])
                
                elif "Backbone" in obj_tags:
                    self.itemconfig(canvas_id, fill = "#2A2226")
                
                elif "TransitOperator" in obj_tags:
                    self.itemconfig(canvas_id, fill = "#1E2422")
                
                elif "Operator" in obj_tags:
                    self.itemconfig(canvas_id, fill = "#232A22")
            
            self.dtag("highlight_path")


    def select_path_nodes(self) -> None:
        '''
        Fonction qui permet à l'utilisateur de créer une connexion entre deux Nodes du Network (précédemment créer)
        '''
        self.deselect_object()
        
        self.config(highlightbackground = "#ffcc22", highlightthickness = 5) 
        nodes = []

        while len(nodes) < 2:                                                   # tant qu'on a deux nodes dans le network, les connexions sont possibles
            if self.selected_node:
                nodes.append(self.selected_node)
                self.selected_node = None
            self.app.parent.update()

        self.config(highlightthickness = 0)
        return nodes


    def highlight_path(self, path : list[Node]) -> None:
        '''
        Fonction qui va permettre de mettre en évidence le plus court chemin entre deux nœuds
        '''
        self.selected_node = path[0]
        self.deselect_object()
        self.selected_node = path[-1]
        self.deselect_object()
            
        
        for node_index in range(len(path) - 1):
            node : Node = path[node_index]
            next_node : Node = path[node_index + 1]

            line_ids = set(self.find_withtag(node.name)).intersection(set(self.find_withtag(next_node.name)))
            for canvas_id in line_ids:
                self.addtag_withtag("highlight_path", canvas_id)
                self.itemconfig(canvas_id, fill = "#FFCC22")

            for node in path:
                self.itemconfig(node.canvas_id, image = self.icons[node.type][1])
                self.addtag_withtag("highlight_path", node.canvas_id)


    def passdown_func(self, arg : str) -> None:
        '''
        Fonction qui va gérer les boutons et leurs actions
        '''
        if arg == "create_network":
            self.create_network_button.place_forget()
            self.app.parent.update()
            
            self.app.info_panel.pack(side = "top", fill = "x")


            print("creating nodes")
            self.nodes_creation()

            print("creating connections")
            self.connect_nodes()

            print("creating routing tables")
            start = time()
            self.create_routing_tables()
            end = time()
            print(f"Created routing tables in {end - start : 0.2f}s")

            self.app.info_panel.set_object_info(self)
        
        elif arg == "find_path":
            nodes = self.select_path_nodes()
            path = self.reconstruct_path(*nodes)
            self.highlight_path(path)
            self.app.info_panel.set_path_info(path, self.calc_path_weight(path))

        elif arg == "check_connectivity":
            conectivity = False
            try: conectivity = self.main_dfs()
            except: pass
            
            self.app.alert = ("Success", "IsConnex") if conectivity else ("Error", "IsNotConnex")
            self.event_generate("<<Alert>>")

        elif arg == "generate_network":
            self.delete("obj")
            self.app.info_panel.path_display.delete("obj")
            self.app.parent.update()

            self.nodes = []
            self.connections = {}
            self.tier1_nodes = []
            self.tier2_nodes = []
            self.tier3_nodes = []
            self.canvas_id_to_node = {}
            Tier1.instance_counter, Tier2.instance_counter, Tier3.instance_counter = 0, 0, 0

            self.app.info_panel.set_object_info(self)
            print("creating nodes")
            self.nodes_creation()

            print("creating connections")
            self.connect_nodes()

            print("creating routing tables")
            start = time()
            self.create_routing_tables()
            end = time()
            print(f"Created routing tables in {end - start : 0.2f}s")
            
            self.app.info_panel.set_object_info(self)