import re
from Term import Term, NTERM_REGEX, TERM_REGEX

RULE_REGEX = f'{NTERM_REGEX}[ \t]*->[ \t]*[a-z](?:{TERM_REGEX})*'

class Rule:
    def __init__(self, left_side, right_side):
        if not left_side.is_nterm() or len(right_side) == 0:
            raise Exception('Incorrect rule definition')
        
        self.left_side = left_side
        self.right_side = right_side
    
    def right_side_nterms_count(self):
        return sum([term.is_nterm() for term in self.right_side])
    
    def parse(rule):
        if not re.fullmatch(RULE_REGEX, rule):
            return None
        
        left, right = map(str.strip, rule.split('->'))
        left_side = Term(left)
        right_side = list(map(Term, list(right)))

        return Rule(left_side, right_side)

    def is_recursive(self):
        return self.left_side in self.right_side

    def right_side_to_str(self) -> str:
        return ''.join(map(str, self.right_side))
    
    def is_right_linear(self) -> bool:
        return bool(re.fullmatch(f'[a-z]+({NTERM_REGEX}|)', self.right_side_to_str()))
    
    def is_constant(self):
        for term in self.right_side:
            if term.is_nterm():
                return False
        return True
    
    def __eq__(self, rule):
        return self.left_side == rule.left_side and self.right_side == rule.right_side
    
    def __getitem__(self, index):
        if index == 0:
            return self.left_side
        return self.right_side[index - 1]

    def __contains__(self, term):
        return term == self.left_side or term in self.right_side
    
    def __str__(self) -> str:
        return f'{self.left_side} → {self.right_side_to_str()}'