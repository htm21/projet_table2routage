


class Node:                                         # création de la class mère (woooow)
    def __init__(self, *, node_type : str, node_id : int, canvas_id : int) -> None:     
        self.type = node_type                       # ça nous servira pour connaître le type de nœuds
        self.id = node_id                           # chaque nœuds aura un id propre à son type
        self.routing_table = {}                     # contiendra la table de routage du Nœud 

        self.backbone_connections = 0               # Nombre de connection de T1     
        self.transit_opertator_connections = 0      # Nombre de connection de T2
        self.opertator_connections = 0              # Nombre de connection de T3

        self.canvas_id = canvas_id
        self.name = self.type + f" {self.id}"       

    def __repr__(self) -> str:
        return f"{self.type} n°{self.id}"                                           # pour un meilleur affichage (évite les noms super bizares)


class Tier1(Node):                                   # La class Tier1 qui hérite de "Node"
    instance_counter = 0                                                            

    def __init__(self, *args, **kwargs) -> None:                 
        Tier1.instance_counter += 1                 # on augmente le nombre d'instance à chaque création de Tier1
        super().__init__(node_type = "Backbone", node_id = self.instance_counter, *args, **kwargs)                   # on hérite la class Mère, et on place le node_type = "Tier1"
          

class Tier2(Node):                                   # De la même façon la class Tier2, le reste suit la même logique
    instance_counter = 0

    def __init__(self, *args, **kwargs) -> None:
        Tier2.instance_counter += 1
        super().__init__(node_type = "TransitOperator", node_id = self.instance_counter, *args, **kwargs)


class Tier3(Node):                                  # De la même façon la class Tier3, le reste suit la même logique
    instance_counter = 0

    def __init__(self, *args, **kwargs) -> None:
        Tier3.instance_counter += 1
        super().__init__(node_type = "Operator", node_id = self.instance_counter, *args, **kwargs)
