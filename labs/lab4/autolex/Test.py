from CFG import CFG
from ipywidgets import Tab, HTML

class Test:
	TESTS = []
	
	def __init__(self, name, test_path):
		self.name = name
		self.test_path = test_path
		self.successful = False
	
	def display_results():
		tab = Tab()

		for test in Test.TESTS:
			index = int(test.name.split('_')[1])
			tab.set_title(index - 1, f'Test {index}')
		tab.children = list(map(Test.get_result, Test.TESTS))

		return tab
	
	def _display_guarded_cfg(cfg, guarded_cfg):
		if cfg == guarded_cfg:
			return ''
		
		return (
			f'''
			<p>
				<b>Обертка охранными нетерминалами</b><br>
				 {guarded_cfg.html()}
			</p>
			'''
		)
	
	def _display_regexes(regexes):
		if len(regexes) == 0:
			return 'Токены <font color=\"tomato\"><b>не найдены</b></font>'
		
		return (
			f'''
			<b>Регулярные выражения для токенов</b><br>
			{"<br>".join([str(token) + " = " + str(regex) for token, regex in regexes.items()])}
			'''
		)	
	
	def _display_conflicted(conflicted):
		if len(conflicted) == 0:
			return '<b>Конфликтующие нетерминалы <font color=\"green\">не найдены</font></b>'
		
		return (
			f'''
			<b><font color=\"orange\">Конфликтующие</font> нетерминалы</b><br>
			{"<br>".join([str(nterm) for nterm in conflicted])}
			'''
		)

	def get_result(self):
		raw_cfg_html = self.raw_cfg.replace('\n', '<br>')

		if not self.successful:
			return HTML(
				f'''
				<div>
					<p>
						<b>Входные данные</b><br>
						{raw_cfg_html}
					</p>
					<p>
						<font color=\"red\"><b>Ошибка:</b></font> грамматика 
						не соответствует синтаксису входных данных.
					</p>
				</div>
				'''
			)
		return HTML(
			f'''
			<div>
				<p>
					<b>КС-грамматика</b><br>
					{self.cfg.html()}
				</p>
				{Test._display_guarded_cfg(self.cfg, self.guarded_cfg)}
				<p>
					{Test._display_conflicted(self.conflicted)}
				</p>
				<p>
					{Test._display_regexes(self.regexes)}
				</p>
			</div>
			'''
		)
	
	def add(test):
		Test.TESTS.append(test)
	
	def execute(self, executor):
		with open(self.test_path) as f:
			self.raw_cfg = f.read()
		
		try:
			self.cfg = CFG.parse(self.raw_cfg)
		except Exception:
			return
		
		result = executor(self.cfg)

		self.guarded_cfg = result[0]
		self.regexes = result[1]
		self.conflicted = result[2]

		self.successful = True
	
	def clear_tests():
		Test.TESTS = []