# Лабораторная работа 2

## Эквивалентные регулярные выражения
Написать три эквивалентных (описывающих один и тот же язык) регулярных выражения:
академическое; с использованием отрицания; с использованием ленивой итерации Клини. \
Минимальная длина regex — $10$ символов.\
Сравнить производительность этих regex на $10$ тестах длиной от $100$ до $10^5$ символов.

## Алгоритм решения системы регуярных выражений
Реализовать алгоритм решения системы регулярных
выражений с беззвездными коэффициентами.

**Синтаксис входных данных:**\
Элементы метаязыка выделены черным цветом, красным — элементы языка входных данных.\
$
\begin{align*}
    \langle system \rangle &::= \langle equation \rangle^{+} \\
    \langle equation \rangle &::= \langle var \rangle \textcolor{red}{\textbf{=}} (\langle regex \rangle \langle var \rangle(\textcolor{red}{\textbf{+}}\langle regex \rangle \langle var \rangle)^*\textcolor{red}{\textbf{+}})?\langle regex \rangle \\
    \langle regex \rangle &::= \textcolor{red}{(}\langle expr \rangle\textcolor{red}{\textbf{|}}\langle alt.regex \rangle\textcolor{red}{)} \; | \; \langle expr \rangle \\
    \langle alt.regex \rangle &::= \langle expr \rangle\textcolor{red}{\textbf{|}}\langle alt.regex \rangle \; | \; \langle expr \rangle \\
    \langle expr \rangle &::= \langle letter \rangle \langle expr \rangle \; | \; \langle letter \rangle \\
    \langle var \rangle &::= \textcolor{red}{A} \; | \; ... \; | \; \textcolor{red}{Z} \\
    \langle letter \rangle &::= \textcolor{red}{a} \; | \; ... \; | \; \textcolor{red}{z}
\end{align*}
$

## Алгоритм преобразования DFA в regex
Реализовать алгоритм преобразования DFA в regex.

**Синтаксис входных данных:**\
$
\begin{align*}
    \langle DFA \rangle &::= \textcolor{red}{\textbf{<}}\langle state \rangle\textcolor{red}{,\{}\langle transition \rangle^{+}\textcolor{red}{\},\{}\langle state \rangle(\textcolor{red}{,}\langle state \rangle)^{*}\textcolor{red}{\}\textbf{>}}\\
    \langle transition \rangle &::= \textcolor{red}{\textbf{<}}\langle state \rangle\textcolor{red}{,}\langle letter \rangle\textcolor{red}{,}\langle state \rangle\textcolor{red}{\textbf{>}} \\
    \langle state \rangle &::= (\textcolor{red}{A} \; | \; ... \; | \; \textcolor{red}{Z})(\textcolor{red}{0} \; | \; ... \; | \; \textcolor{red}{9})? \\
    \langle letter \rangle &::= \textcolor{red}{a} \; | \; ... \; | \; \textcolor{red}{z}
\end{align*}
$\
Первое состояние в списке — начальное. Список состояний в фигурных скобках задает множество конечных состояний. Список всех состояний явно не перечисляется, он восстанавливается по правилам перехода.