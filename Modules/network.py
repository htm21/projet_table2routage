from Modules.custom_button import *
from Modules.utils import *
from Modules.node import *                  # On importe les class des Nœuds créé pour pouvoir les utilisés
from itertools import combinations

import tkinter as tk
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

        self.connections : dict[Node : list] = {}               # un Network contient des connections entre Nodes (c.f Association des Nodes)
        self.nodes : list[Node] = []              # un Network contient aussi une liste de Nodes (ça serait bête sinon)
        
        self.tier1_nodes : list[Node] = []
        self.tier2_nodes : list[Node] = []
        self.tier3_nodes : list[Node] = []



    def nodes_creation(self) -> None :      # La fonction qui va créer nos Nodes de manère uniforme !!
        
        boundries = set_node_boundries(self.winfo_width() // 2, (self.winfo_height() // 2) - 50)

        for _ in range(10) :
            x, y = choose_coords(boundries, "Backbone")
            overlap = self.find_overlapping(x - 45, y - 45, x + 45, y + 45)
            while overlap:
                x, y = choose_coords(boundries, "Backbone")
                overlap = self.find_overlapping(x - 45, y - 45, x + 45, y + 45)

            canvas_id = self.create_image(x, y, image = self.icons["Backbone"][0], tags = "node")               # On veut 10 Tier1
            node = Tier1(canvas_id = canvas_id)
    
            self.nodes.append(node)         # on l'ajoute à la liste des Nodes
            self.connections[node] = []     # création d'une clé pour pouvoir connaître les connections de chaque Node
            self.tier1_nodes.append(node)
            self.canvas_id_to_node[canvas_id] = node
        

        for _ in range(20) :
            x, y = choose_coords(boundries, "TransitOperator")
            overlap = self.find_overlapping(x - 35, y - 35, x + 35, y + 35)
            while overlap:
                x, y = choose_coords(boundries, "TransitOperator")
                overlap = self.find_overlapping(x - 35, y - 35, x + 35, y + 35)

            canvas_id = self.create_image(x, y, image = self.icons["TransitOperator"][0], tags = "node")
            node = Tier2(canvas_id = canvas_id)
            
            self.nodes.append(node)
            self.connections[node] = []
            self.tier2_nodes.append(node)
            self.canvas_id_to_node[canvas_id] = node
        

        for _ in range(70) :
            x, y = choose_coords(boundries, "Operator")
            overlap = self.find_overlapping(x - 20, y - 20, x + 20, y + 20)
            while overlap:
                x, y = choose_coords(boundries, "Operator")
                overlap = self.find_overlapping(x - 20, y - 20, x + 20, y + 20)
            
            canvas_id = self.create_image(x, y, image = self.icons["Operator"][0], tags = "node")
            node = Tier3(canvas_id = canvas_id)
            
            self.nodes.append(node)
            self.connections[node] = []
            self.tier3_nodes.append(node)
            self.canvas_id_to_node[canvas_id] = node


    #########################################################################################################################################################
    ######################################## CRÉATION DU GRAPHE NON ORIENTÉ DU RÉSEAU ########################################################################
    #########################################################################################################################################################

    def connect_nodes(self) -> None:
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
                
                node_1.backbone_connections += 1 ; node_2.backbone_connections += 1
                self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 5, fill = "#2A2226", smooth = True, tags = ["Backbone", f"{node_1.name}", f"{node_2.name}"])


    def connect_tier_2_nodes(self) -> None:
        ''' Fonction qui gère les connections des Tier2 '''

        for node_1 in self.tier2_nodes:                         # on parcours les Tier2
            
            backbone_connections = rd.randint(1, 2)
            while backbone_connections != 0:
                node_2 = rd.choice(self.tier1_nodes) 
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]):
                    poids = rd.randint(10, 20) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    
                    node_1.backbone_connections += 1 ; node_2.backbone_connections += 1
                    backbone_connections -= 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 3, fill = "#1E2422", smooth = True, tags = ["TransitOperator", f"{node_1.name}", f"{node_2.name}"])

            transit_opertator_connections = rd.randint(2, 3)    # Même logique pour les liens T2-T2
            while transit_opertator_connections != 0:
                node_2 = rd.choice(self.tier2_nodes)
                if not any([node_2 is connection[0] for connection in self.connections[node_1]]) and node_1 is not node_2:
                    poids = rd.randint(10, 20) 
                    self.connections[node_1].append((node_2, poids)); self.connections[node_2].append((node_1, poids))
                    
                    node_1.transit_opertator_connections += 1 ; node_2.transit_opertator_connections += 1
                    transit_opertator_connections -= 1
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
                    
                    node_1.transit_opertator_connections += 1 ; node_2.opertator_connections += 1
                    opertator_connections -= 1
                    self.create_line((*self.coords(node_1.canvas_id), *self.coords(node_2.canvas_id)), width = 1, fill = "#232A22", smooth = True, tags = ["Operator", f"{node_1.name}", f"{node_2.name}"])


######################################## COMMENT VERIFIER SI UN GRAPH EST CONNEXE ? PARCOURS EN LARGEUR OU PROFONDEUR ########################################################################

    

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


    # GUI Functions ====================================================================



    def select_object(self, event):
        object_ids = self.find_overlapping(event.x, event.y, event.x, event.y) # Finds canvas item closest to cursor      
        if not object_ids: self.deselect_object(); return
        if self.selected_node: self.deselect_object()
        if not "node" in self.gettags(object_ids[-1]): self.deselect_object(); return

        node = self.canvas_id_to_node[object_ids[-1]]
        self.selected_node = node
        print(node.routing_table)
        line_ids = self.find_withtag(node.name)
        for line_id in line_ids:
            self.itemconfig(line_id, fill = "#FFCC22")


        self.event_generate("<<ObjControls>>")
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
        self.event_generate("<<ObjControls>>")
        self.dtag("selected")


    def passdown_func(self, arg) -> None:
        if arg == "create_network":
            self.app.info_panel.pack(side = "top", fill = "x")
            self.create_network_button.place_forget()
            
            print("creating nodes")
            self.nodes_creation()
            print("creating connections")
            self.connect_nodes()
            print("creating routing tables")
            for node in self.nodes:
                node.routing_table = self.next_hop(node)