import re

NTERM_REGEX = r'[A-Z][0-9]*'
TERM_REGEX = f'{NTERM_REGEX}|[a-z]'

class Term:
    def __init__(self, term):
        if not re.fullmatch(TERM_REGEX, term):
            raise Exception('Incorrect term')
        self.term = term
    
    def _to_index(number):
        index = ''
        for digit in number:
            index += chr(ord('\u2080') | int(digit))
        return index
    
    def is_nterm(self) -> bool:
        return bool(re.fullmatch(NTERM_REGEX, self.term))
    
    def __eq__(self, term) -> bool:
        return self.term == term.term
    
    def __hash__(self) -> int:
        return hash(self.term)
    
    def __str__(self) -> str:
        if self.is_nterm():
            if len(self.term) == 1:
                return self.term
            return self.term[0] + Term._to_index(self[1:])
        return self.term
    