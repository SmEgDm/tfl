from CFG import CFG
from Term import Term
from graphviz import Digraph

ID = 0

class Node:
    def __init__(self, term: Term) -> None:
        global ID
        self.term = term
        self.children = []
        self.id = ID
        ID += 1
    
    def add_child(self, child) -> None:
        self.children.append(child)
    
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

class PumpTree:
    def _pump_term(term, start_nterm, cfg, visited):
        if not term.is_nterm():
            return (Node(term), False)
        
        if term in visited:
            return (Node(term), True) if term == start_nterm else (None, False)

        for rule in cfg.rules_with_left_side(term):
            node = Node(term)
            found = False
            for child_term in rule.right_side:
                if found:
                    child = Node(child_term)
                else:
                    visited.add(term)
                    child, found = PumpTree._pump_term(
                        child_term, 
                        start_nterm, 
                        cfg, 
                        visited
                    )
                    if child == None:
                        break
                node.add_child(child)
            if found:
                return (node, True)
        
        return (None, False)

    def __init__(self, cfg: CFG, start_nterm: Term):
        global ID
        ID = 0

        self.root, _ = PumpTree._pump_term(
            start_nterm,
            start_nterm,
            cfg,
            set()
        )
    
    def get_pumping(self):
        pumping = self.root.get_pumping()
        separator_index = pumping.index(self.root.term)

        return pumping[0:separator_index], pumping[separator_index + 1:]

    def to_graphviz(self):
        digraph = Digraph(format='svg')
        self.root.to_graphviz(digraph)
        return digraph

