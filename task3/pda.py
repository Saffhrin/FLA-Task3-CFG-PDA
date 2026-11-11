"""General nondeterministic PDA simulator with instantaneous descriptions."""
from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class PDATransition:
    source: str
    input_symbol: str | None  # None is ε
    stack_top: str | None    # None means the stack must be empty
    destination: str
    push: tuple[str, ...] = ()  # appended bottom-to-top after removing stack_top


@dataclass(frozen=True)
class Configuration:
    state: str
    input_index: int
    stack: tuple[str, ...]


@dataclass(frozen=True)
class PDAStep:
    configuration: Configuration
    action: str


@dataclass(frozen=True)
class PDAResult:
    accepted: bool
    explored_configurations: int
    steps: tuple[PDAStep, ...]
    limit_reached: bool = False


class PDA:
    def __init__(
        self,
        *,
        states: Iterable[str],
        input_alphabet: Iterable[str],
        stack_alphabet: Iterable[str],
        start_state: str,
        initial_stack: Iterable[str],
        transitions: Iterable[PDATransition],
        accepting_states: Iterable[str] = (),
        accept_by_empty_stack: bool = False,
    ) -> None:
        self.states = frozenset(states)
        self.input_alphabet = frozenset(input_alphabet)
        self.stack_alphabet = frozenset(stack_alphabet)
        self.start_state = start_state
        self.initial_stack = tuple(initial_stack)
        self.transitions = tuple(transitions)
        self.accepting_states = frozenset(accepting_states)
        self.accept_by_empty_stack = accept_by_empty_stack
        by_key: dict[tuple[str, str | None, str | None], list[PDATransition]] = defaultdict(list)
        for transition in self.transitions:
            by_key[(transition.source, transition.input_symbol, transition.stack_top)].append(transition)
        self._by_key = by_key

    @property
    def is_deterministic(self) -> bool:
        by_state_stack: dict[tuple[str, str | None], list[PDATransition]] = defaultdict(list)
        for transition in self.transitions:
            by_state_stack[(transition.source, transition.stack_top)].append(transition)
        for choices in by_state_stack.values():
            if any(t.input_symbol is None for t in choices) and len(choices) > 1:
                return False
            symbols = [t.input_symbol for t in choices]
            if len(symbols) != len(set(symbols)):
                return False
        return True

    def run(self, input_symbols: Iterable[str], max_configurations: int = 50_000) -> PDAResult:
        """Explore reachable configurations breadth-first and return an accepting path."""
        symbols = tuple(input_symbols)
        start = Configuration(self.start_state, 0, self.initial_stack)
        pending = deque([start])
        parent: dict[Configuration, tuple[Configuration, str] | None] = {start: None}
        accepting: Configuration | None = None
        while pending:
            current = pending.popleft()
            if current.input_index == len(symbols):
                if self.accept_by_empty_stack and not current.stack:
                    accepting = current
                    break
                if not self.accept_by_empty_stack and current.state in self.accepting_states:
                    accepting = current
                    break
            if len(parent) >= max_configurations:
                return PDAResult(False, len(parent), (), limit_reached=True)
            top = current.stack[-1] if current.stack else None
            candidates = self._by_key.get((current.state, None, top), ())
            if current.input_index < len(symbols):
                candidates = tuple(candidates) + tuple(
                    self._by_key.get((current.state, symbols[current.input_index], top), ())
                )
            for transition in candidates:
                if transition.stack_top is None:
                    if current.stack:
                        continue
                    remaining_stack = current.stack
                else:
                    if not current.stack or current.stack[-1] != transition.stack_top:
                        continue
                    remaining_stack = current.stack[:-1]
                next_index = current.input_index + (transition.input_symbol is not None)
                next_config = Configuration(
                    transition.destination,
                    next_index,
                    remaining_stack + transition.push,
                )
                if next_config not in parent:
                    parent[next_config] = (current, self._describe(transition))
                    pending.append(next_config)
        if accepting is None:
            return PDAResult(False, len(parent), ())
        reverse_steps: list[PDAStep] = []
        cursor = accepting
        while parent[cursor] is not None:
            previous, action = parent[cursor]  # type: ignore[misc]
            reverse_steps.append(PDAStep(cursor, action))
            cursor = previous
        reverse_steps.append(PDAStep(start, "start"))
        reverse_steps.reverse()
        return PDAResult(True, len(parent), tuple(reverse_steps))

    @staticmethod
    def _describe(transition: PDATransition) -> str:
        inp = "ε" if transition.input_symbol is None else repr(transition.input_symbol)
        top = "empty" if transition.stack_top is None else repr(transition.stack_top)
        push = "ε" if not transition.push else " ".join(transition.push)
        return f"δ({transition.source}, {inp}, {top}) → ({transition.destination}, {push})"


def cfg_to_pda(productions: dict[str, tuple[tuple[str, ...], ...]], start: str, terminals: Iterable[str]) -> PDA:
    """Construct the standard one-state CFG-to-NPDA (accept by empty stack)."""
    nonterminals = set(productions)
    terminal_set = set(terminals)
    transitions: list[PDATransition] = []
    for nonterminal, alternatives in productions.items():
        for rhs in alternatives:
            transitions.append(PDATransition("q", None, nonterminal, "q", tuple(reversed(rhs))))
    for terminal in terminal_set:
        transitions.append(PDATransition("q", terminal, terminal, "q", ()))
    return PDA(
        states={"q"},
        input_alphabet=terminal_set,
        stack_alphabet=nonterminals | terminal_set,
        start_state="q",
        initial_stack=(start,),
        transitions=transitions,
        accept_by_empty_stack=True,
    )


def balanced_parentheses_pda() -> PDA:
    """Deterministic one-type parenthesis PDA accepting by empty stack."""
    transitions = (
        PDATransition("q", "(", None, "q", ("(",)),
        PDATransition("q", "(", "(", "q", ("(", "(")),
        PDATransition("q", ")", "(", "q", ()),
    )
    return PDA(
        states={"q"}, input_alphabet={"(", ")"}, stack_alphabet={"("},
        start_state="q", initial_stack=(), transitions=transitions,
        accept_by_empty_stack=True,
    )
