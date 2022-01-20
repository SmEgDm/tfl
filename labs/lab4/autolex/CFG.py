import re
from tokenize import Token
from Rule import Rule
from copy import copy

class CFG:
    CFG_REGEX = f'([ \t\n])*({Rule.RULE_REGEX}([ \t\n])*)+'

    def _find_nterms(rules):
        nterms = set()
        for rule in rules:
            nterms.add(rule.left)
            for token in rule.right:
                if token.is_nterm():
                    nterms.add(token)
        
        return nterms

    def __init__(self, start_nterm, rules):
        self.start_nterm = start_nterm
        self.rules = rules
        self.nterms = CFG._find_nterms(rules)
        self.first = {}
        self.follow = {}
        self.last = {}
        self.precede = {}
    
    def parse(raw_cfg):
        if not re.fullmatch (CFG.CFG_REGEX, raw_cfg):
            raise Exception('Incorrect CFG')
        
        rules = list(map(Rule.parse, re.findall(Rule.RULE_REGEX, raw_cfg)))

        return CFG(rules[0].left, rules)
    
    def _filter_rules(self, nterms):
        result = []
        for rule in self.rules:
            is_useless = False
            for token in rule:
                if token.is_nterm() and token not in nterms:
                    is_useless = True
                    break
            if not is_useless:
                result.append(rule)
        
        self.rules = result
        self.nterms = nterms
    
    def filter_generating_nterms(self):
        generating_nterms = set()
        while True:
            previous_generating_nterms = generating_nterms.copy()
            for rule in self.rules:
                is_generating = True
                for token in rule.right:
                    if token.is_nterm() and token not in generating_nterms:
                        is_generating = False
                        break
                if is_generating:
                    generating_nterms.add(rule.left)
            
            if previous_generating_nterms == generating_nterms:
                break
        
        self._filter_rules(generating_nterms)
    
    def filter_reachable_nterms(self):
        reachable_nterms = set([self.start_nterm])
        while True:
            previous_reachable_nterms = reachable_nterms.copy()
            for rule in self.rules:
                if rule.left not in reachable_nterms:
                    continue
                for token in rule.right:
                    if token.is_nterm():
                        reachable_nterms.add(token)
            
            if previous_reachable_nterms == reachable_nterms:
                break
        
        self._filter_rules(reachable_nterms)
    
    def filter_useful_nterms(self):
        self.filter_generating_nterms()
        self.filter_reachable_nterms()
    
    def regular_subset(self, indicator):
        result = set()
        for nterm in self.nterms:
            is_regular = True
            for rule in self[nterm]:
                if not indicator(rule):
                    is_regular = False
            if is_regular:
                result.add(nterm)
        
        while True:
            previous_result = result.copy()
            irregular_nterms = set()
            for nterm in result:
                for rule in self[nterm]:
                    for token in rule.right:
                        if token.is_nterm() and token not in result:
                            irregular_nterms.add(nterm)
            
            for nterm in irregular_nterms:
                if nterm in result:
                    result.remove(nterm)
            
            if result == previous_result:
                break
        
        return result

    def regular_closure(self, regular_subset):
        result = regular_subset.copy()
    
        while True:
            previous_result = result.copy()
            for nterm in self.nterms:
                if nterm in result:
                    continue

                is_regular = True
                for rule in self[nterm]:
                    for token in rule.right:
                        if token.is_nterm() and token not in result:
                            is_regular = False
                
                if is_regular:
                    result.add(nterm)
            
            if result == previous_result:
                break
        
        return result
    
    def regular_nterms(self):
        return self.regular_closure(
            self.regular_subset(Rule.is_left_linear)
            .union(self.regular_subset(Rule.is_right_linear))
        )

    def html(self):
        return '<br>'.join(map(str, self.rules))
    
    def __eq__(self, cfg):
        if self.start_nterm != cfg.start_nterm:
            return False
        
        for rule in self.rules:
            if rule not in cfg.rules:
                return False
        
        for rule in cfg.rules:
            if rule not in self.rules:
                return False
        
        return True
    
    def __copy__(self):
        start_nterm = copy(self.start_nterm)
        rules = []
        for rule in self.rules:
            rules.append(copy(rule))
        
        return CFG(start_nterm, rules)

    def __getitem__(self, nterm):
        return [rule for rule in self.rules if rule.left == nterm]
    
    def __str__(self) -> str:
        return '\n'.join(map(str, self.rules))