#!/usr/bin/env python
# coding: utf-8

# # Проверка конфлюэнтности по перекрытию

# ## Парсер

# In[1]:


import re

rule_format = r'[ \t]*([a-z]+)[ \t]*->[ \t]*([a-z]*)[ \t]*'

def parse(lines):
    srs = []
    for line in lines:
        if line == '': continue
        if not re.fullmatch(rule_format, line):
            raise Exception(f'The rule \"{line}\" has incorrect format')
        srs.append(list(map(lambda x: x.strip(), line.split('->'))))
    return srs


# ## Проверка на перекрытие

# In[2]:


def has_overlap(term, other_term=None):
    if other_term == None:
        for i in range(1, len(term) // 2 + 1):
            if term[:i] == term[-i:]:
                return True
        return False
    for i in range(min(len(term), len(other_term)) + 1):
        if term[i:] == other_term[-i:] or term[-i:] == other_term[i:]:
            return True
    return False


# ## Проверка конфлюэнтности

# In[3]:


def confluence_verdict(srs):
    for i in range(len(srs)):
        if has_overlap(srs[i][0]):
            return ('The system may not be confluence', f'Overlapping term: {srs[i][0]}')
        for j in range(i + 1, len(srs)):
            if has_overlap(srs[i][0], srs[j][0]):
                return ('The system may not be confluence', f'Overlapping terms: {srs[i][0]}, {srs[j][0]}')
    return ('The system is confluence', None)


# ## Тесты

# In[4]:


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
    with open(f'tests/test_{i}.txt') as f:
        lines = [line.strip() for line in f.readlines() if line != '\n']
        result = ''
        try:
            srs = parse(lines)
            verdict, overlap = confluence_verdict(srs)
            result =  f'{verdict}<br>{overlap if overlap != None else ""}'
        except Exception as err:
            result = f'<b>Parse error: </b>{err}'
        children.append(output_pattern('<br>'.join(lines), result))

tab = Tab()
for i in range(tests_count):
    tab.set_title(i, f'Test {i + 1}')
tab.children = children

tab


# In[ ]:




