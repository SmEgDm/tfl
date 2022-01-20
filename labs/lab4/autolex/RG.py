from Rule import Rule
from CFG import CFG
import Regex
import Equation
import re
from Token import Token

def parse_symbol(tokens):
    if re.fullmatch(Token.TERM_REGEX, tokens[0]):
        return Regex.Regex(Regex.Operation.CONST, tokens.pop(0))

Regex.Regex.set_parse_symbol(parse_symbol)
Regex.Regex.set_one('ε')
Regex.Regex.set_zero('Ø')

class RG(CFG):
	def __init__(self, start_nterm, rules):
		super().__init__(start_nterm, rules)
	
	def from_cfg(cfg, start_nterm):
		rg = RG(start_nterm, cfg.rules)
		rg.filter_reachable_nterms()
		return rg
	
	def to_right_linear(self):
		for rule in self.rules:
			if self.start_nterm in rule.right:
				new_start_nterm = self.start_nterm.quote()
				self.rules.append(Rule(new_start_nterm, [self.start_nterm]))
				self.start_nterm = new_start_nterm
				break
		
		rules = []
		for rule in self.rules:
			if rule.is_terminal():
				if rule.left == self.start_nterm:
					rules.append(rule)
				else:
					rules.append(Rule(self.start_nterm, rule.right + [rule.left]))
			else:
				if rule.left == self.start_nterm:
					rules.append(Rule(rule.right[0], rule.right[1:]))
				else:
					rules.append(Rule(rule.right[0], rule.right[1:] + [rule.left]))
		
		self.rules = rules
		self.nterms = RG._find_nterms(rules)
	
	def to_regex(self):
		system = []
		for nterm in self.nterms:
			var = str(nterm)
			lin_comb = {}
			for rule in self[nterm]:
				if rule.is_epsilon():
					if '' in lin_comb:
						lin_comb[''] += Regex.Regex('')
					else:
						lin_comb[''] = Regex.Regex('')
				elif rule.is_terminal():
					if '' in lin_comb:
						lin_comb[''] += Regex.Regex.parse(rule.right_str())
					else:
						lin_comb[''] = Regex.Regex.parse(rule.right_str())
				else:
					other_var = str(rule.right[-1])
					coef = Regex.Regex.parse(
                    ''.join([str(token) for token in rule.right[:-1]])
                	)
					if other_var in lin_comb:
						lin_comb[other_var] += coef
					else:
						lin_comb[other_var] = coef
			
			equation = Equation.Equation(var, lin_comb)
			
			system.append(equation)
		
		system = Equation.solve_system(system)

		for equation in system:
			if equation.var == str(self.start_nterm):
				return equation.lin_comb['']

