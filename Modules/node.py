class Node:
    def __init__(self, node_type: str) -> None:
        self.type = node_type
        self.id = None  

    def __repr__(self) -> str:
        return f"{self.type} n°{self.id}"


class Tier1(Node):
    instance_counter = 0

    def __init__(self) -> None:
        super().__init__("Tier1")
        Tier1.instance_counter += 1
        self.id = Tier1.instance_counter


class Tier2(Node):
    instance_counter = 0

    def __init__(self) -> None:
        super().__init__("Tier2")
        Tier2.instance_counter += 1
        self.id = Tier2.instance_counter


class Tier3(Node):
    instance_counter = 0

    def __init__(self) -> None:
        super().__init__("Tier3")
        Tier3.instance_counter += 1
        self.id = Tier3.instance_counter