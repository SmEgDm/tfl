#!/usr/bin/env python
# coding: utf-8

# # Алгоритм унификации линейных термов

# ## Лексер

# In[1]:


def tokenize(line):
    tokens = []
    token = ''
    for symbol in ''.join(line.split()):
        if symbol.isdigit() and token.isdigit() and token != '0':
            token += symbol
            continue
        if token != '': tokens.append(token)
        token = symbol
    if token != '': tokens.append(token)
    
    return tokens


# ## Парсeр конструкторов

# In[2]:


import re

constructor_regex = r'[a-zA-Z][ \t]*\([ \t]*\d+[ \t]*\)'

constructors_regex = f'constructors[ \t]*=[ \t]*({constructor_regex}[ \t]*(,[ \t]*{constructor_regex}[ \t]*)*)?'

def parse_constructors(line):
    if not re.fullmatch(constructors_regex, line):
        raise Exception('Incorrect constructors definition')
    constructors = {}
    constants = set()
    for constructor_str in re.findall(constructor_regex, line):
        name = re.findall(r'[a-zA-Z]', constructor_str)[0]
        args_count = int(re.findall(r'\d', constructor_str)[0])
        if re.fullmatch(r'[a-z]', name):
            if args_count <= 0:
                raise Exception('Argument count of constructor must be a natural number')
            constructors[name] = args_count
        else:
            if args_count != 0:
                raise Exception('Argument count of constant must be zero')
            constants.add(name)
    
    return (constructors, constants)


# ## Парсер переменных

# In[3]:


variables_regex = r'variables[ \t]*=[ \t]*([a-z][ \t]*(,[ \t]*[a-z][ \t]*)*)?'

def parse_variables(line):
    if not re.fullmatch(variables_regex, line):
        raise Exception('Incorrect variables definition')
    
    return set(re.findall(r'[a-z]', line.split('=')[1]))


# ## Парсeр термов

# In[4]:


class Term:
    def __init__(self, name, subterms=[]):
        self.name = name
        self.subterms = subterms
    
    def is_composite(self):
        return len(self.subterms) != 0
    
    def is_variable(self):
        return not self.is_composite() and re.fullmatch(r'[a-z]', self.name)
    
    def __eq__(self, obj):
        return isinstance(obj, Term) and self.name == obj.name

    def __str__(self):
        if self.is_composite():
            result = f'{self.name}({str(self.subterms[0])}'
            for i in range(1, len(self.subterms)):
                result += f', {str(self.subterms[i])}'
            return f'{result})'
        return self.name

class TRS:
    def __init__(self, constructors, constants, variables):
        if len(set(constructors) & variables) != 0:
            raise Exception('Constructors and variables must have different names')
        self.constructors = constructors
        self.constants = constants
        self.variables = variables
    
    def parse_term(self, line):
        tokens = tokenize(line)
        def term():
            if tokens[0] in self.constructors:
                return constructor()
            if tokens[0] in self.variables | self.constants:
                return Term(tokens.pop(0))
            raise Exception('Incorrect term')
        def constructor():
            name = tokens.pop(0)
            if tokens.pop(0) != '(':
                raise Exception('Incorrect term')
            args = [term()]
            def tail():
                if tokens[0] != ',': return
                tokens.pop(0)
                args.append(term())
                tail()
            tail()
            if tokens.pop(0) != ')' or self.constructors[name] != len(args):
                raise Exception('Incorrect term')
            return Term(name, args)
        return term()


# ## Унификатор

# In[5]:


substitutions = []

class UnificationException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

def unification(term, other_term):
    if term.is_variable():
        substitutions.append(f'{str(term)} := {str(other_term)}')
        return other_term
    if other_term.is_variable():
        substitutions.append(f'{str(other_term)} := {str(term)}')
        return term
    if term == other_term:
        return Term(term.name, [unification(term.subterms[i], other_term.subterms[i]) for i in range(len(term.subterms))])
    raise UnificationException('Unable to unificate')


# ## Тесты

# In[6]:


import os
from ipywidgets import Tab, HTML

tests_count = len(os.listdir('tests'))

children = []
output_pattern = lambda input_text, result: HTML(
    f'''
    <div>
        <b>Input</b><br>
        {input_text}<br><br>
        <b>Result</b><br>
        {result}
    </div>
    '''
)

for i in range(tests_count):
    substitutions = []
    with open(f'tests/test_{i}.txt') as f:
        lines = [line.strip() for line in f.readlines() if line != '\n']
        result = ''
        try:
            trs = TRS(*parse_constructors(lines[0]), parse_variables(lines[1]))
            term = trs.parse_term(lines[2].split('=')[1])
            other_term = trs.parse_term(lines[3].split('=')[1])
            unifier = unification(term, other_term)
            result = f'Unifier: {unifier}<br>Substitutions: {"; ".join(substitutions)}'
        except UnificationException as err:
            result = err
        except Exception as err:
            result = f'<b>Parse error: </b>{err}'
        children.append(output_pattern('<br>'.join(lines), result))

tab = Tab()
for i in range(tests_count):
    tab.set_title(i, f'Test {i + 1}')
tab.children = children

tab


# In[ ]:




