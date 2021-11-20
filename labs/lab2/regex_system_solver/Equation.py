import re
import Regex

def parse_var(tokens):
    if len(tokens) != 0 and re.fullmatch(r'[A-Z]', tokens[0]):
        return tokens.pop(0)

class Equation:
    def __init__(self, var, lin_comb):
        self.var = var
        self.lin_comb = {var: lin_comb[var] for var in lin_comb}
        if '' not in self.lin_comb:
            self.lin_comb[''] = Regex.Regex()
    
    def set_parse_var(func):
        global parse_var
        if func == None:
            return
        parse_var = func

    def parse(value):
        global parse_var
        tokens = [token for token in ''.join(value.split())]
        def parse_L():
            if len(tokens) == 0:
                raise Exception('Incorrect equation')
            term = parse_T()
            if len(tokens) == 0:
                return [term]
            if tokens.pop(0) != '+' :
                raise Exception('Incorrect equation')
            return [term] + parse_L()
        def parse_T():
            regex = Regex.Regex.parse(tokens)
            var = parse_var(tokens) 
            return (var if var != None else '', regex)
        var = parse_var(tokens)
        if var == None:
            raise Exception('Incorrect equation')
        if len(tokens) == 0 or tokens.pop(0) != '=':
            raise Exception('Incorrect equation')
        terms = parse_L()
        lin_comb = {}
        for term in terms:
            if term[0] in lin_comb:
                lin_comb[term[0]] += term[1]
                continue
            lin_comb[term[0]] = term[1]
        return Equation(var, lin_comb)
    
    def solve(self):
        if self.var not in self.lin_comb:
            return self
        multiplier = Regex.Regex.kleene_star(self.lin_comb[self.var])
        self.lin_comb = {var: multiplier * coef for var, coef in self.lin_comb.items()}
        del self.lin_comb[self.var]
        return self

    def substitute(self, equation):
        if equation.var not in self.lin_comb:
            return self
        multipiler = self.lin_comb[equation.var]
        del self.lin_comb[equation.var]
        for var in equation.lin_comb:
            if var not in self.lin_comb:
                self.lin_comb[var] = Regex.Regex()
        for var in self.lin_comb:
            if var in equation.lin_comb:
                self.lin_comb[var] += multipiler * equation.lin_comb[var]
        return self
    
    def __str__(self):
        result = f'{self.var} ='
        for var, coef in self.lin_comb.items():
            if coef.is_zero():
                continue
            if coef.is_one():
                result += f' {var} +' if var != '' else f' {coef} +'
                continue
            result += f' {coef}{var} +'
        if result[-1] == '=':
            return f'{result} {self.lin_comb[""]}'
        return result[:-2]

def solve_system(equations):
    n = len(equations)
    for i in range(n):
        for j in range(i):
            equations[i].substitute(equations[j])
        equations[i].solve()
    for i in range(n - 1, -1, -1):
        for j  in range(i + 1, n):
            equations[i].substitute(equations[j])
    return equations