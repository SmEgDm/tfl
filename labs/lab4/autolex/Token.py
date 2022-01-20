import re

class Token:
    NTERM_REGEX = '\\[[a-zA-Z]+\'?\\]'
    TERM_REGEX = '[a-z]|[0-9]|_|\\*|\\+|=|\\(|\\)|\\$|;|:|\\^|/|\\-'
    TOKEN_REGEX = f'{NTERM_REGEX}|{TERM_REGEX}'

    def __init__(self, value):
        if not re.fullmatch(Token.TOKEN_REGEX, value):
            raise Exception('Incorrect token')
        
        self.value = value
        self.is_guard = False
        self.is_token = False
    
    def is_term(self):
        return not self.is_guard and bool(re.fullmatch(Token.TERM_REGEX, self.value))
    
    def is_nterm(self):
        return self.is_guard or bool(re.fullmatch(Token.NTERM_REGEX, self.value))
    
    def quote(self):
        return Token(f'[{str(self.value)[1:-1]}\']')
    
    def __copy__(self):
        token_copy = Token(self.value)
        token_copy.is_guard = self.is_guard
        token_copy.is_token = self.is_token

        return token_copy
    
    def __eq__(self, token):
        return (
            self.value == token.value and
            self.is_guard == token.is_guard and
            self.is_token == token.is_token
        )
    
    def __hash__(self):
        return hash(self.value)
    
    def __str__(self):
        if self.is_guard:
            return f'[GUARD{self.value}]'
        return self.value
    