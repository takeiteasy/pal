from typing import Optional
from .node import NodeType

class ParentNode:
    def __init__(self):
        self.children = []

    def add_child(self, node: NodeType):
        self.children.append(node)

    def add_children(self, nodes: NodeType | list[NodeType]):
        for node in nodes if isinstance(nodes, list) else [nodes]:
            self.add_child(node)

    def get_children(self, name: Optional[str] = ""):
        return [x for x in self.children if x.name == name]

    def rem_children(self, name: Optional[str] = ""):
        self.children = [x for x in self.children if x.name != name]

    def clear_children(self):
        self.children = []
