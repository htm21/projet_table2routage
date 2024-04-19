import random as rd

class Node:
    def __init__(self, node_type: str) -> None:     # LA CLASS MÈRE WOWWW
        self.type = node_type                       # ça nous servira pour connaître le type de nœuds
        self.id = None                              # chaque nœuds aura un id propre à son type
        self.nt1 = None                             
        self.nt2 = None

    def __repr__(self) -> str:
        return f"{self.type} n°{self.id}"           # pour un meilleur affichage (évite les noms super bizares)


class Tier1(Node):                                  # La class Tier1 qui hérite de "Node"
    instance_counter = 0                            # va nous permettre de donner des id ≠ pour chaque entité de Tier1

    def __init__(self) -> None:                 
        super().__init__("Tier1")                   # on hérite la class Mère, et on place le node_type = "Tier1"
        Tier1.instance_counter += 1                 # on augmente le nombre d'instance à chaque création de Tier1
        self.id = Tier1.instance_counter            # on l'associe à l'id, genre 2eme Tier1 aura l'id : 2
        self.nt2 = 4            


class Tier2(Node):                                  # De la même façon la class Tier2, le reste suit la même logique
    instance_counter = 0

    def __init__(self) -> None:
        super().__init__("Tier2")
        Tier2.instance_counter += 1
        self.id = Tier2.instance_counter
        self.nt1 = rd.randint(1,2)
        self.nt2 = rd.randint(2,3)
        self.nt3 = 4



class Tier3(Node):
    instance_counter = 0

    def __init__(self) -> None:
        super().__init__("Tier3")
        Tier3.instance_counter += 1
        self.id = Tier3.instance_counter
        self.nt2 = 2
    
