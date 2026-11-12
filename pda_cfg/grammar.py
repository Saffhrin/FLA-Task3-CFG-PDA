"""Context-free grammar analysis: FIRST/FOLLOW and LL(1) table construction."""
from dataclasses import dataclass
from typing import Mapping

EPSILON = "ε"
END = "$"
Production = tuple[str, ...]


@dataclass(frozen=True)
class Grammar:
    start: str
    terminals: frozenset[str]
    productions: Mapping[str, tuple[Production, ...]]

    @property
    def nonterminals(self) -> frozenset[str]:
        return frozenset(self.productions)


@dataclass(frozen=True)
class GrammarAnalysis:
    first: Mapping[str, frozenset[str]]
    follow: Mapping[str, frozenset[str]]
    table: Mapping[tuple[str, str], Production]
    conflicts: Mapping[tuple[str, str], tuple[Production, ...]]


EXPRESSION_GRAMMAR = Grammar(
    start="E",
    terminals=frozenset({"id", "+", "*", "(", ")", "="}),
    productions={
        "S": (("id", "=", "E"),),
        "E": (("T", "Ep"),),
        "Ep": (("+", "T", "Ep"), ()),
        "T": (("F", "Tp"),),
        "Tp": (("*", "F", "Tp"), ()),
        "F": (("(", "E", ")"), ("id",)),
    },
)


def first_of_sequence(sequence: Production, first: Mapping[str, set[str]], terminals: frozenset[str]) -> set[str]:
    if not sequence:
        return {EPSILON}
    result: set[str] = set()
    for symbol in sequence:
        if symbol in terminals:
            result.add(symbol)
            return result
        symbol_first = first[symbol]
        result.update(symbol_first - {EPSILON})
        if EPSILON not in symbol_first:
            return result
    result.add(EPSILON)
    return result


def analyze(grammar: Grammar) -> GrammarAnalysis:
    """Compute FIRST, FOLLOW, predictive table, and any LL(1) conflicts."""
    first = {nonterminal: set() for nonterminal in grammar.nonterminals}
    changed = True
    while changed:
        changed = False
        for lhs, alternatives in grammar.productions.items():
            for rhs in alternatives:
                before = len(first[lhs])
                first[lhs].update(first_of_sequence(rhs, first, grammar.terminals))
                changed |= len(first[lhs]) != before

    follow = {nonterminal: set() for nonterminal in grammar.nonterminals}
    follow[grammar.start].add(END)
    changed = True
    while changed:
        changed = False
        for lhs, alternatives in grammar.productions.items():
            for rhs in alternatives:
                for i, symbol in enumerate(rhs):
                    if symbol not in grammar.nonterminals:
                        continue
                    suffix_first = first_of_sequence(rhs[i + 1:], first, grammar.terminals)
                    before = len(follow[symbol])
                    follow[symbol].update(suffix_first - {EPSILON})
                    if EPSILON in suffix_first or i + 1 == len(rhs):
                        follow[symbol].update(follow[lhs])
                    changed |= len(follow[symbol]) != before

    entries: dict[tuple[str, str], list[Production]] = {}
    for lhs, alternatives in grammar.productions.items():
        for rhs in alternatives:
            predict = first_of_sequence(rhs, first, grammar.terminals)
            lookaheads = predict - {EPSILON}
            if EPSILON in predict:
                lookaheads |= follow[lhs]
            for lookahead in lookaheads:
                entries.setdefault((lhs, lookahead), []).append(rhs)
    conflicts = {key: tuple(rhs_list) for key, rhs_list in entries.items() if len(rhs_list) > 1}
    table = {key: rhs_list[0] for key, rhs_list in entries.items() if len(rhs_list) == 1}
    return GrammarAnalysis(
        first={key: frozenset(value) for key, value in first.items()},
        follow={key: frozenset(value) for key, value in follow.items()},
        table=table,
        conflicts=conflicts,
    )


GRAMMAR_ANALYSIS = analyze(EXPRESSION_GRAMMAR)
