import re
from Token import Token
from copy import copy

class Rule:
    ARROW_REGEX = r'::='
    RULE_REGEX = (
        f'{Token.NTERM_REGEX}'
        f'[ \t]*{ARROW_REGEX}[ \t]*'
        f'(?:(?:{Token.TOKEN_REGEX})[ \t]*)+'
    )

    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def parse(raw_rule):
        if not re.fullmatch(Rule.RULE_REGEX, raw_rule):
            raise Exception('Incorrect rule')
        
        raw_left, raw_right = map(str.strip, raw_rule.split(Rule.ARROW_REGEX))

        return Rule(
            Token(raw_left), 
            list(map(Token, re.findall(f'(?:{Token.TOKEN_REGEX})', raw_right)))
        )
    
    def right_str(self):
        return ''.join(map(str, self.right))
    
    def is_left_linear(self):
        return bool(
            re.fullmatch(
                f'({Token.NTERM_REGEX}|)({Token.TERM_REGEX})*', 
                self.right_str()
            )
        )
    
    def is_right_linear(self):
        return bool(
            re.fullmatch(
                f'({Token.TERM_REGEX})*({Token.NTERM_REGEX}|)', 
                self.right_str()
            )
        )
    
    def partitions(self):
        result = []
        for i in range(len(self.right)):
            if self.right[i].is_nterm():
                result.append(
                    (self.right[i], (self.right[:i], self.right[i + 1:]))
                )
        return result

    
    def is_terminal(self):
        for token in self.right:
            if token.is_nterm():
                return False
        
        return True
    
    def is_epsilon(self):
        return len(self.right) == 0
    
    def __copy__(self):
        left = copy(self.left)
        right = []
        for token in self.right:
            right.append(copy(token))
        
        return Rule(left, right)

    def __hash__(self):
        return hash((self.left, self.right))
    
    def __getitem__(self, index):
        if index == 0:
            return self.left
        
        return self.right[index - 1]
    
    def __eq__(self, rule):
        return self.left == rule.left and self.right == rule.right

    def __contains__(self, term):
        return term == self.left or term in self.right
    
    def __str__(self):
        return f'{self.left} {Rule.ARROW_REGEX} {self.right_str()}'