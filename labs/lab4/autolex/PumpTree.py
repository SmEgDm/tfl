import Regex
import re
from Token import Token

def parse_symbol(tokens):
    if re.fullmatch(Token.TERM_REGEX, tokens[0]):
        return Regex.Regex(Regex.Operation.CONST, tokens.pop(0))

Regex.Regex.set_parse_symbol(parse_symbol)
Regex.Regex.set_one('ε')
Regex.Regex.set_zero('Ø')

class Node():
	def __init__(self, label, children):
		self.label = label
		self.children = children

class PumpTree():
	def _dfs(cfg, pump, regexes):
		is_leaf = True
		for token in pump:
			if token.is_nterm() and token not in regexes:
				is_leaf = False
				break
		
		if is_leaf:
			return Node(pump, [])
		
		children = []
		for i in range(len(pump)):
			if pump[i].is_term() or pump[i] in regexes:
				continue

			for rule in cfg[pump[i]]:
				child = PumpTree._dfs(
					cfg, 
					pump[:i] + rule.right + pump[i + 1:],
					regexes
				)
				children.append(child)
		
		return Node(pump, children)

	def __init__(self, cfg, nterm, regexes):
		children = [PumpTree._dfs(cfg, rule.right, regexes) for rule in cfg[nterm]]
		self.root = Node(nterm, children)
		self.regexes = regexes

	def leaves(self):
		def dfs(node, current_leaves):
			if len(node.children) == 0:
				current_leaves.append(node.label)
				return
			
			for child in node.children:
				dfs(child, current_leaves)
		
		result = []
		dfs(self.root, result)

		return result
	
	def generate_regex(self):
		result = Regex.Regex()
		for leaf in self.leaves():
			regex = Regex.Regex('')
			for token in leaf:
				if token in self.regexes:
					regex *= self.regexes[token]
				else:
					regex *= Regex.Regex.parse(str(token))
			result += regex
		
		return result