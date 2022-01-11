from Term import Term
from graphviz import Digraph

ID = 0

class Node:
    def __init__(self, term: Term) -> None:
        self.term = term
        self.children = []
        self.id = Node.next_id()

    def next_id():
        global ID
        id = ID
        ID += 1

        return id
    
    def set_id(id):
        global ID
        ID = id
    
    def get_id():
        global ID

        return ID
    
    def add_child(self, child) -> None:
        self.children.append(child)
    
    def add_children(self, children):
        for child in children:
            self.add_child(child)
        
    def cut(self, nterm):
        def rec(node):
            if node.term == nterm:
                self.children = []
                return
            for child in self.children:
                rec(child)
        rec(self)
    
    def amogus(self, nterm):
        found = False
        def rec(node):
            nonlocal found

            if node.term == nterm:
                found = True
            if not found:
                for child in node.children:
                    rec(child)
        rec(self)

        return found
    
    def is_leaf(self):
        return len(self.children) == 0
    
    def get_pumping(self):
        if self.is_leaf():
            return [self.term]
        pumping = []
        for child in self.children:
            pumping += child.get_pumping()
        return pumping

    def to_graphviz(self, digraph):
        digraph.node(str(self.id), str(self.term), shape='circle')
        for child in self.children:
            child.to_graphviz(digraph)
            digraph.edge(str(self.id), str(child.id))