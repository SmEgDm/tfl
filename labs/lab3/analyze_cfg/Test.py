from CFG import CFG
from ipywidgets import Tab, HTML
from graphviz import Digraph
import os

TESTS = []

TREES_PATH = 'trees'

TREES_PATH_GITHUB = "https://raw.githubusercontent.com/SmEgDm/tfl/main/labs/lab3/analyze_cfg"

class Test:
    def __init__(self, name, test_path):
        self.name = name
        self.test_path = test_path
        self.successful = False
    
    def display_results():
        global TESTS

        tab = Tab()
        for test in TESTS:
            index = int(test.name.split('_')[1])
            tab.set_title(index - 1, f'Test {index}')
        tab.children = list(map(Test.get_result, TESTS))

        return tab
    
    def _display_nterms(nterms, type):
        if len(nterms) != 0:
            return (
                f'''
                    <b>{type}</b> нетерминалы: {
                        ", ".join([str(nterm) for nterm in nterms])
                    }<br>
                '''
            )
        return ''
    
    def _display_tree(tree):
        return (
            f'''
                <img src=\'{tree[1]}\' alt={tree[0]}>
            '''
        )
    
    def _display_trees(self):
        if len(self.rendered_trees) == 0:
            return ''
        return (
            f'''
            <p>
                <b>Деревья подозрительных накачек</b><br>
                {' '.join(map(Test._display_tree, self.rendered_trees))}
            </p>
            '''
        )
    
    def _display_verdict(self):
        if self.cfg.start_nterm in self.regular_clousure:
            return 'Язык <font color=\"green\"><b>регулярен</b></font>'
        elif self.cfg.start_nterm in self.possibly_regular_clousure:
            return 'Язык <font color=\"orange\"><b>возможно регулярен</b></font>'
        elif self.cfg.start_nterm in self.suspicious_nterms:
            return 'Язык <font color=\"tomato\"><b>подозрительный</b></font>'
        else:
            return '<font color=\"red\"><b>Не удалось определить тип языка</b></font>'

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
                <p>
                    {Test._display_nterms(
                        self.regular_clousure, 
                        'Регулярные'
                    )}
                    {Test._display_nterms(
                        self.possibly_regular_clousure, 
                        'Возможно регулярные'
                    )}
                    {Test._display_nterms(
                        self.suspicious_nterms, 
                        'Подозрительные'
                    )}
                    {self._display_trees()}
                    <p>{self._display_verdict()}</p>
                </p>
            </div>
            '''
        )

    def _render_trees(self):
        global TREES_PATH, TREES_PATH_GITHUB

        self.rendered_trees = []

        for tree in self.trees:
            tree.to_graphviz().render(filename=os.path.join(
                TREES_PATH,
                self.name,
                str(tree.root.term)
            ))
            self.rendered_trees.append((
                f'{self.name}_{tree.root.term}',
                os.path.join(
                    TREES_PATH_GITHUB,
                    self.name, 
                    str(tree.root.term)
                ) + '.svg'
            ))
    
    def execute(self, executor):
        global TESTS

        with open(self.test_path) as f:
            self.raw_cfg = f.read()
        
        try:
            self.cfg = CFG.parse(self.raw_cfg)
        except Exception:
            TESTS.append(self)
            return
        
        result = executor(self.cfg)

        self.regular_clousure = result[0]
        self.possibly_regular_clousure = result[1]
        self.suspicious_nterms = result[2]
        self.trees = result[3]

        self._render_trees()

        self.successful = True

        TESTS.append(self)
    
    def clear_tests():
        global TESTS

        TESTS = []


