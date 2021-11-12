import re
from enum import Enum, auto

class Operation(Enum):
    CONST = auto()
    ALT = auto()
    CONCAT = auto()
    KLEENE = auto()

ZERO = '0'
ONE = '1'

def parse_symbol(tokens):
    if re.fullmatch('[a-z01]', tokens[0]):
        return Regex(Operation.CONST, tokens.pop(0))

class Regex():
    def __init__(self, operation=None, operands=ZERO):
        global ONE, ZERO
        if operation == None:
            self.operation = Operation.CONST
            self.operands = ZERO
        elif operation == '':
            self.operation = Operation.CONST
            self.operands = ONE
        else:
            self.operation = operation
            self.operands = operands
    
    def parse(value):
        global parse_symbol
        tokens = [token for token in value] if isinstance(value, str) else value
        def parse_S():
            regex = parse_T1()
            if len(tokens) != 0 and tokens[0] == '|':
                tokens.pop(0)
                other_regex = parse_S()
                return regex + other_regex
            return regex
        def parse_T1():
            regex = parse_T2()
            if regex == Regex(''):
                return regex
            other_regex = parse_T1()
            if other_regex != Regex(''):
                return regex * other_regex
            return regex
        def parse_T2():
            regex = parse_T3()
            if regex == Regex(''):
                return regex
            if len(tokens) != 0 and tokens[0] == '*':
                tokens.pop(0)
                return regex.kleene_star()
            return regex
        def parse_T3():
            if len(tokens) == 0:
                return Regex('')
            regex = parse_symbol(tokens)
            if regex != None:
                return regex
            if tokens[0] == '(':
                tokens.pop(0)
                regex = parse_S()
                if len(tokens) != 0 and tokens.pop(0) == ')':
                    return regex
                raise Exception('Incorrect regex')
            return Regex('')
        regex = parse_S()
        if isinstance(value, str) and len(tokens) != 0:
            raise Exception('Incorrect regex')
        return regex
    
    def __eq__(self, regex):
        return isinstance(regex, Regex) and self.operation == regex.operation and self.operands == regex.operands
    
    def set_zero(value):
        global ZERO
        if value == None:
            return
        ZERO = value
    
    def set_one(value):
        global ONE
        if value == None:
            return
        ONE = value
    
    def set_parse_symbol(func):
        global parse_symbol
        if func == None:
            return
        parse_symbol = func
    
    def is_zero(self):
        global ZERO
        return self.operation == Operation.CONST and self.operands == ZERO
    
    def is_one(self):
        global ONE
        return self.operation == Operation.CONST and self.operands == ONE
    
    def kleene_star(regex):
        global ONE
        if regex.is_zero() or regex.is_one():
            return Regex('')
        if regex.operation == Operation.KLEENE:
            return regex
        return Regex(Operation.KLEENE, regex)

    def __add__(self, regex):
        if self.is_zero():
            return regex
        if regex.is_zero():
            return self 
        self_operands = [self]
        if self.operation == Operation.ALT:
            self_operands = self.operands
        regex_operands = [regex]
        if regex.operation == Operation.ALT:
            regex_operands = regex.operands
        operands = []
        for operand in self_operands + regex_operands:
            if operand not in operands:
                operands.append(operand)
        return Regex(Operation.ALT, operands)
    
    def __mul__(self, regex):
        if self.is_zero() or regex.is_zero():
            return Regex()
        if self.is_one():
            return regex
        if regex.is_one():
            return self
        self_operands = [self]
        if self.operation == Operation.CONCAT:
            self_operands = self.operands
        regex_operands = [regex]
        if regex.operation == Operation.CONCAT:
            regex_operands = regex.operands
        return Regex(Operation.CONCAT, self_operands + regex_operands)
    
    def __str__(self):
        match self.operation:
            case Operation.CONST:
                return self.operands
            case Operation.KLEENE:
                if self.operands.operation == Operation.CONST:
                    return f'{self.operands}*'
                return f'({self.operands})*'
            case Operation.CONCAT:
                result = ''
                for operand in self.operands:
                    if operand.operation == Operation.ALT:
                        result += f'({operand})'
                        continue
                    result +=  f'{operand}'
                return result
            case Operation.ALT:
                return '|'.join(map(str, self.operands))