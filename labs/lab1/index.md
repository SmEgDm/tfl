# Лабораторная работа 1

## Алгоритм унификации линейных термов
Дана сигнатура для TRS. Написать алгоритм
унификации линейных термов в этой сигнатуре.

**Синтаксис входных данных:**
<p>
	constructors = ([буква]([нат. число]),)∗ [буква]([нат. число]))<br>
	variables = ([буква],)∗[буква]<br>
	first = [терм]<br>
	second = [терм]<br>
	[терм] ::= [переменная] | [константа] | [конструктор](([терм],) ∗[терм])
</p>


[Реализация](./trs_unification/index.ipynb)

## Проверка конфлюэнтности по перекрытию
Дана SRS. Написать алгоритм проверки ее конфлюэнтности по перекрытию.

**Синтаксис входных данных:**
<p>([буква]∗ -> [буква]∗ $)+</p>

[Реализация](./srs_confluence/index.ipynb)
