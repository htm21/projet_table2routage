from Modules.custom_button import *
from Modules.utils import *
from Modules.node import *                  # On importe les class des Nœuds créé pour pouvoir les utilisés
from itertools import combinations          # On importe la fonction combinations de itertools pour faciliter la formation de liens (cf connect_tier_1_nodes())

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
            "Connectivity" : (load_to_size("connectivity", 65, 65), load_to_size("highlight_connectivity", 65, 65)),
            "Path" : (load_to_size("path", 65, 65), load_to_size("highlight_path", 65, 65)),
            "NewNetwork" : (load_to_size("network", 65, 65), load_to_size("highlight_network", 65, 65)),
            }

        self.selected_node : Node = None
        self.bind("<Button-1>", self.select_object)

        self.create_network_button = CustomButton(parent = self, parent_obj = self, func_arg = "create_network", icons = self.icons["Network"], image = self.icons["Network"][0], compound = "top", text = "Create\nNetwork", justify = "center", font = f"{font} 28 bold", foreground = "#FFFFFF", background = self.kwargs["background"])
        self.create_network_button.place(anchor = "center", relx = 0.5, rely = 0.5)

        self.network_tools = tk.Frame(self, background = "#22282a")
        self.buffer_frame_1 = tk.Frame(self.network_tools, background = "#1D2123", height = 5)
        self.buffer_frame_2 = tk.Frame(self.network_tools, background = "#1D2123", width = 5)
        self.find_path_button = CustomButton(parent = self.network_tools, parent_obj = self, func_arg = "find_path", icons = self.icons["Path"], image = self.icons["Path"][0], background = "#22282a")
        self.connectivity_button = CustomButton(parent = self.network_tools, parent_obj = self, func_arg = "check_connectivity", icons = self.icons["Connectivity"], image = self.icons["Connectivity"][0], background = "#22282a")
        self.generate_network = CustomButton(parent = self.network_tools, parent_obj = self, func_arg = "generate_network", icons = self.icons["NewNetwork"], image = self.icons["NewNetwork"][0], background = "#22282a")

        self.buffer_frame_1.pack(side = "top", fill = "x")
        self.buffer_frame_2.pack(side = "left", fill = "y")
        self.generate_network.pack(side = "right", padx = 15, pady = 15)
        self.connectivity_button.pack(side = "right", padx = 15, pady = 15)
        self.find_path_button.pack(side = "right", padx = 15, pady = 15)
        
        # Logic Stuff ==================================================================

        self.connections : dict[Node : list[Node]] = {}               # un Network contient des connections entre Nodes (c.f Association des Nodes)
        self.nodes : list[Node] = []              # un Network contient aussi une liste de Nodes (ça serait bête sinon)
        
        self.tier1_nodes : list[Node] = []                      # création d'une liste qui contiendra les Tier1
        self.tier2_nodes : list[Node] = []                      # ... Tier2
        self.tier3_nodes : list[Node] = []                      # ... Tier3



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

            canvas_id = self.create_image(x, y, image = self.icons["Backbone"][0], tags = "node")          
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

            canvas_id = self.create_image(x, y, image = self.icons["TransitOperator"][0], tags = "node")
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
            
            canvas_id = self.create_image(x, y, image = self.icons["Operator"][0], tags = "node")
            node = Tier3(canvas_id = canvas_id)             # initialisation du Node
            
            self.nodes.append(node)                         # on l'ajoute à la liste des Nodes
            self.connections[node] = []                     # création d'une clé pour pouvoir connaître les connections de chaque Node
            self.tier3_nodes.append(node)                   # on ajoute le Node à la liste des Tier1 (permettra de s'organiser lors des connections inter node)
            self.canvas_id_to_node[canvas_id] = node


    #########################################################################################################################################################
    ######################################## CRÉATION DU GRAPHE NON ORIENTÉ DU RÉSEAU ########################################################################
    #########################################################################################################################################################

    def connect_nodes(self) -> None:
        ''' Fonction qui créer le graphe non orienté contenant les 3 types de Tier, avec des liens pondérés '''
        self.connect_tier_1_nodes()                                                             
        self.connect_tier_2_nodes()
        self.connect_tier_3_nodes()

        self.tag_raise("TransitOperator")
        self.tag_raise("Backbone")
        self.tag_raise("node")


    def connect_tier_1_nodes(self) -> None:
        ''' Fonction qui gère les connections des Tier1 '''
        possible_connections = int((10 * (10 - 1)) / 2)
        node_combinizations = list(combinations(self.tier1_nodes, 2))
        connections = [rd.random() < 0.75 for _ in range(possible_connections)]         # connections possibles T1-T1 avec une probabilité de 75%

        for index, connection in enumerate(connections):                             
            if connection:
                poids = rd.randint(5, 10)
                node_1, node_2 = node_combinizations[index][0], node_combinizations[index][1]
                self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                
                self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 5, fill = "#2A2226", smooth = True, tags = ["Backbone", f"{node_1.name}", f"{node_2.name}"])

        for node in self.tier1_nodes:
            node.backbone_connections += len(self.connections[node])


    def connect_tier_2_nodes(self) -> None:
        ''' Fonction qui gère les connections des Tier2 '''

        for node_1 in self.tier2_nodes:                         # on parcours les Tier2
            
            backbone_connections = rd.randint(1, 2)             # on génère un nombre aléatoire de connections aux Tier1 (1 ou 2)
            while backbone_connections != 0:                    # on boucle tant qu'une connection est disponible 
                node_2 = rd.choice(self.tier1_nodes)            # on prends un Tier1 aléatoirement (grâce à rd.choice() dans la liste)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):                       # si aucune connection entre les deux nœuds est active 
                    poids = rd.randint(10, 20)                                                                          # génère un poids entre 10 et 20 (car implique un Tier2)
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))  # on ajoute la connections dans les deux nœuds     
                    
                    backbone_connections -= 1
                    node_1.backbone_connections += 1; node_2.transit_opertator_connections += 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 3, fill = "#1E2422", smooth = True, tags = ["TransitOperator", f"{node_1.name}", f"{node_2.name}"])
            
            transit_opertator_connections = rd.randint(2, 3) - node_1.transit_opertator_connections   # Même logique pour les liens T2-T2
            while transit_opertator_connections > 0:
                node_2 = rd.choice(self.tier2_nodes)            # on choisi un Tier2 aléatoirement 
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]) and node_1 is not node_2 and node_2.transit_opertator_connections <= 2:  # Même logique
                    poids = rd.randint(10, 20)                                                                              # ...
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))      
                    
                    transit_opertator_connections -= 1
                    node_1.transit_opertator_connections += 1; node_2.transit_opertator_connections += 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 3, fill = "#1E2422", smooth = True, tags = ["TransitOperator", f"{node_1.name}", f"{node_2.name}"])

    
    def connect_tier_3_nodes(self) -> None:
        ''' Fonction qui gère les connections des Tier3 '''

        for node_1 in self.tier3_nodes:                 # on parcours les Tier3
            opertator_connections = 2                   # chaque Tier3 a 2 connections disponibles 
            while opertator_connections != 0:           # tant qu'on peut connecter
                node_2 = rd.choice(self.tier2_nodes)    # on choisi des Tier2 aléatoires (Rappel T3 <-> T2 seulement)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):     # on vérifie si le Tier2 n'est pas déjà lié au Tier3
                    poids = rd.randint(20, 50)                                                        # dans ce cas là -> génération d'un poids aléatoire entre 20 et 50
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))  # on ajoute les liens des deux sens (non-orienté)

                    opertator_connections -= 1
                    node_1.transit_opertator_connections += 1; node_2.opertator_connections += 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 1, fill = "#232A22", smooth = True, tags = ["Operator", f"{node_1.name}", f"{node_2.name}"])


##############################################################################################################################################################################
######################################## COMMENT VERIFIER SI UN GRAPH EST CONNEXE ? GRÂCE AUX PARCOURS ########################################################################
##############################################################################################################################################################################
    

    def PP(self, traiter, node) -> None :
        ''' Fonction PP qui va faire le parcours en profondeur du Noeud en entrée et de ses voisins en les stockant '''    
        if node not in traiter :                       
            traiter.append(node)                       # si le Noeud n'est pas dans la liste traiter alors on l'ajoute
            for connection in self.connections[node] : # on regard ses connections
                self.PP(traiter, connection[0])        # et on effectue à leur tour un parcours en profondeur
    
    def main_dfs(self) -> bool :
        ''' Fonction main du parcours en largeur, elle va créer la liste qui contiendra tout les noeuds atteint '''
        traiter = []                                   # inventaire des noeuds "marquer"
        depart = self.nodes[rd.randint(1,100)]         # il nous faut une racine pour démarer (on prend aléatoirement)
        self.PP(traiter, depart)                       # on lance la fonction PP récursive
        
        return len(traiter) == len(self.nodes)         # on vérifie si la longueur de la liste "traiter" est égale la taille de la liste contenant tout les nodes (self.nodes)


##############################################################################################################################################################################
####################################################### TABLES DE ROUTAGE ---> NEXT HOP ######################################################################################
##############################################################################################################################################################################


    def next_hop(self, start_node) -> dict[Node : Node]:
        ''' Fonction qui forme la table de routage pour le noeud en entrée, utilisation de https://www.youtube.com/watch?v=LGiRB_lByh0&t=1027s '''
        
        distance = {node : float("inf") for node in self.connections}           # comme dans djikstra, on fixe tout les noeuds à distance "infini" 
        distance[start_node] = 0                                                # alors que le node de départ "start_node" est nul

        next_hope = {node : None for node in self.connections}                  # de même pour le prochain noeud, ils sont tous nuls au départ
        next_hope[start_node] = start_node                                      # le prochain noeud pour atteindre le noeud de départ est lui même
        
        unvisited = set(self.connections.keys())                                # set qui permettra de vérifier quels Nodes on déjà étaient visités

        while unvisited :
            current_node = min(unvisited, key= lambda node : distance[node])    # mini par rapport à leur distance, on prendra toujours start_node en premier car sa distance vaudra toujours 0
            unvisited.remove(current_node)                                      # Node visiter, on le retire alors du set des non-visité

            for neighbor, weight in self.connections[current_node] :            # on parcours les connections du Node actuel en séparant Tier(neighbor) et poids(weight)
                if neighbor in unvisited :                                     
                    new_dist = distance[current_node] + weight                  # on calcul la distance, si elle est meilleure (plus faible) => on mets à jour

                    if new_dist < distance[neighbor] :                          # dans djikstra, si la val est inférieur au poids actuelle
                        distance[neighbor] = new_dist                           # -> on la modifie, sinon on passe

                    if current_node == start_node :                             # si connecté au noeud de départ
                        next_hope[neighbor] = neighbor                          # alors le prochain noeud pour atteindre son voisin est lui même
                    else :
                        next_hope[neighbor] = next_hope[current_node]           # sinon on place comme prochain noeud, le prochain noeud du noeud actuel
                        
        return next_hope                                                        # on renvoie la table de routage du start_node


    def shortest_weighted_path(self, start_node, end_node) -> list[Node]:
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
        path.append(start_node); path.reverse()
        return path
    
    
    def create_routing_tables(self):
        for start_node in self.nodes:
            index = 0
            while len(start_node.routing_table) != len(self.nodes) - 1:
                end_node : Node = self.nodes[index]
                
                if not start_node.routing_table.get(end_node):
                    path = self.shortest_weighted_path(start_node, end_node)
                    for index_node in range(len(path) - 1):
                        sub_node : Node = path[index_node]
                        sub_node.routing_table[end_node] = path[index_node + 1]
                index += 1


    def reconstruct_path(self, start : Node, end : Node) -> list[Node]: 

        path, node, pointer = [start], start, end

        while node is not end:
            print(f"Next node {node.routing_table[pointer]}")
            node = node.routing_table[pointer]
            path.append(node)
        
        return path


    # GUI Functions ====================================================================



    def select_object(self, event : tk.Event):
        object_ids = self.find_overlapping(event.x, event.y, event.x, event.y) # Finds canvas item closest to cursor      
        
        if not object_ids: 
            self.deselect_object()
            self.app.info_panel.set_object_info(self)
            return
        
        if self.selected_node: 
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
                self.deselect_object()
            self.app.parent.update()

        self.config(highlightthickness = 0)
        return nodes


    def passdown_func(self, arg : str) -> None:
        if arg == "create_network":
            self.create_network_button.place_forget()
            self.app.info_panel.pack(side = "top", fill = "x")
            self.network_tools.place(anchor = "se", relx = 1, rely = 1)
 
            self.nodes_creation()
            self.connect_nodes()
            print("creating routing tables")
            self.create_routing_tables()

            self.app.info_panel.set_object_info(self)
        
        elif arg == "find_path":
            nodes = self.select_path_nodes()
            print(f"Is connexe : {self.main_dfs()}")
            print(f"Selected Nodes : {nodes}")
            print(f"Path to take : {self.reconstruct_path(*nodes)}")
        
        elif arg == "check_connectivity":
            pass
        
        elif arg == "generate_network":
            pass


