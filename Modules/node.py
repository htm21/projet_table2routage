import random as rd

class Node :
    instance_counter : int = 0

    def __init__(self, name : str, type : str) -> None:
        Node.instance_counter += 1
        self.name = name
        self.id = Node.instance_counter
        self.type = type


class Tier1(Node) : 
    instance_counter : int = 0
    def __init__(self, name : str, type : str = "Tier1") -> None:
        super().__init__(name, type)
        Node.instance_counter += 1
        Tier1.instance_counter += 1


class Tier2(Node):
    instance_counter : int = 0

    def __init__(self, name : str, type : str = "Tier2") -> None:
        super().__init__(name, type)
        Node.instance_counter += 1
        Tier2.instance_counter += 1


class Tier3(Node) :
    instance_counter : int = 0

    def __init__(self, name : str, type: str = "Tier3") -> None:
        super().__init__(name, type)
        Node.instance_counter += 1
        Tier3.instance_counter += 1