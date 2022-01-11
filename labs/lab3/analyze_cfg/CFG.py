import re
from Rule import Rule, RULE_REGEX
from Node import Node

CFG_REGEX = f'([ \t]|\n)*({RULE_REGEX}([ \t]|\n)*)+'

class CFG:
    def __init__(self, start_nterm, rules):
        self.start_nterm = start_nterm
        self.rules = rules
    
    def parse(raw_cfg):
        if not re.fullmatch (CFG_REGEX, raw_cfg):
            raise Exception('Incorrect CFG')
        rules = list(map(Rule.parse, re.findall(RULE_REGEX, raw_cfg)))

        return CFG(rules[0].left_side, rules)
    
    def get_nterms(self):
        nterms = set()
        for rule in self:
            nterms.add(rule.left_side)
            for term in rule.right_side:
                if term.is_nterm():
                    nterms.add(term)
        return nterms

    def rules_with_left_side(self, nterm):
        return [rule for rule in self if nterm == rule.left_side]

    def get_filtered_rules(self, filter):
        rules = []
        for rule in self:
            is_useless_rule = False
            for term in rule:
                if term.is_nterm() and not filter[term]:
                    is_useless_rule = True
                    break
            if not is_useless_rule:
                rules.append(rule)

        return rules
    
    def _filter_generating_nterms(self):
        nterms = self.get_nterms()
        is_generating = {nterm: False for nterm in nterms}
        counter = {rule: rule.right_side_nterms_count() for rule in self}
        concerned_rules = {
            nterm: [rule for rule in self if nterm in rule.right_side] 
            for nterm in nterms
        }
        queue = [rule.left_side for rule in self if counter[rule] == 0]
        for nterm in queue:
            is_generating[nterm] = True

        while len(queue) != 0:
            nterm = queue.pop()
            for rule in concerned_rules[nterm]:
                counter[rule] -= 1
                if counter[rule] == 0:
                    queue.append(rule.left_side)
                    is_generating[rule.left_side] = True
        
        self.rules = self.get_filtered_rules(is_generating)
    
    def _filter_reachable_nterms(self):
        nterms = self.get_nterms()
        is_reachable = {nterm: False for nterm in nterms}

        def dfs(nterm):
            is_reachable[nterm] = True
            for rule in self.rules_with_left_side(nterm):
                for term in rule.right_side:
                    if term.is_nterm() and not is_reachable[term]:
                        dfs(term)
        
        dfs(self.start_nterm)

        self.rules = self.get_filtered_rules(is_reachable)
    
    def filter_useful_nterms(self):
        #self._filter_generating_nterms()
        self._filter_reachable_nterms()
    
    def get_constant_nterms(self):
        constant_nterms = set()
        for rule in self:
            if rule.is_constant():
                constant_nterms.add(rule.left_side)
        
        return constant_nterms

    def get_flp_parse_trees(self):
        nterms = self.get_nterms()
        trees = {}
        for rule in self:
            if rule.is_constant() and rule.left_side not in trees:
                node = Node(rule.left_side)
                node.add_children([Node(term) for term in rule.right_side])
                trees[rule.left_side] = node

        while len(trees) != len(nterms):
            rules = []
            for rule in self:
                if rule.left_side not in trees:
                    rules.append(rule)
            
            def count(rule):
                return sum([term not in trees for term in rule.right_side if term.is_nterm()])

            rules = sorted(rules, key=count)

            while len(rules) != 0:
                print('-----')
                rule = rules.pop(0)
                if rule.left_side not in trees:
                    children = []
                    for term in rule.right_side:
                        if term.is_nterm():
                            if term not in trees:
                                children = []
                                break
                            children.append(trees[term])
                    if len(children) == 0:
                        continue
                    node = Node(rule.left_side)
                    node.add_children(children)
                    trees[rule.left_side] = node
        
        return trees

    def html(self):
        return '<br>'.join(map(str, self.rules))

    def __getitem__(self, index):
        return self.rules[index]
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.rules))