class Node:
    def __init__(self, node_type : str, node_id : int) -> None:                     # LA CLASS MÈRE WOWWW
        self.type = node_type                                                       # ça nous servira pour connaître le type de nœuds
        self.id = node_id                                                           # chaque nœuds aura un id propre à son type
        
        self.backbone_connections = 0                             
        self.transit_opertator_connections = 0
        self.opertator_connections = 0

    def __repr__(self) -> str:
        return f"{self.type} n°{self.id}"                                           # pour un meilleur affichage (évite les noms super bizares)


class Tier1(Node):                                                                  # La class Tier1 qui hérite de "Node"
    instance_counter = 0                                                            # va nous permettre de donner des id ≠ pour chaque entité de Tier1

    def __init__(self) -> None:                 
        Tier1.instance_counter += 1                                                 # on augmente le nombre d'instance à chaque création de Tier1
        super().__init__(node_type = "Tier1", node_id = self.instance_counter)      # on hérite la class Mère, et on place le node_type = "Tier1"
          

class Tier2(Node):                                                                  # De la même façon la class Tier2, le reste suit la même logique
    instance_counter = 0

    def __init__(self) -> None:
        Tier2.instance_counter += 1
        super().__init__(node_type = "Tier2", node_id = self.instance_counter)


class Tier3(Node):
    instance_counter = 0

    def __init__(self) -> None:
        Tier3.instance_counter += 1
        super().__init__(node_type = "Tier3", node_id = self.instance_counter)