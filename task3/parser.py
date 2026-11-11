"""Predictive grammar parser implemented as a deterministic PDA stack."""
from dataclasses import dataclass
import re

TOKEN_RE = re.compile(r"\s*([A-Za-z_][A-Za-z0-9_]*|[0-9]+|[=+*()]|.)")
TABLE = {
    ("S", "id"): ("id", "=", "E"),
    ("E", "id"): ("T", "Ep"), ("E", "("): ("T", "Ep"),
    ("T", "id"): ("F", "Tp"), ("T", "("): ("F", "Tp"),
    ("F", "id"): ("id",), ("F", "("): ("(", "E", ")"),
    ("Ep", "+"): ("+", "T", "Ep"), ("Ep", ")"): (), ("Ep", "$"): (),
    ("Tp", "*"): ("*", "F", "Tp"), ("Tp", "+"): (),
    ("Tp", ")"): (), ("Tp", "$"): (),
}
NONTERMINALS = frozenset({"S", "E", "Ep", "T", "Tp", "F"})
TERMINALS = frozenset({"id", "=", "+", "*", "(", ")", "$"})


@dataclass(frozen=True)
class StackStep:
    stack_top_first: tuple[str, ...]
    input_remaining: tuple[str, ...]
    action: str


@dataclass(frozen=True)
class ParseResult:
    accepted: bool
    trace: tuple[str, ...]
    error: str | None = None
    steps: tuple[StackStep, ...] = ()


def tokenize(source: str) -> list[str]:
    source = source.strip()
    tokens: list[str] = []
    pos = 0
    while pos < len(source):
        match = TOKEN_RE.match(source, pos)
        if not match:
            raise ValueError(f"Cannot tokenize input at position {pos}")
        raw = match.group(1)
        if raw.isspace():
            pos = match.end()
            continue
        if raw.isidentifier() or raw.isascii() and raw.isdigit():
            tokens.append("id")
        elif raw in "=+*()":
            tokens.append(raw)
        else:
            raise ValueError(f"Unexpected character {raw!r} at position {pos}")
        pos = match.end()
    return tokens


def parse(source: str, *, assignment: bool = False) -> ParseResult:
    """Parse a full expression, or an assignment statement, and retain PDA moves."""
    try:
        tokens = tokenize(source) + ["$"]
    except ValueError as exc:
        return ParseResult(False, (), str(exc))
    stack = ["$", "S" if assignment else "E"]
    cursor = 0
    trace: list[str] = []
    steps: list[StackStep] = []
    while stack:
        top = stack.pop()
        lookahead = tokens[cursor]
        if top in NONTERMINALS:
            production = TABLE.get((top, lookahead))
            if production is None:
                error = f"No production for {top} with lookahead {lookahead}"
                steps.append(StackStep(tuple(reversed(stack + [top])), tuple(tokens[cursor:]), f"reject: {error}"))
                return ParseResult(False, tuple(trace), error, tuple(steps))
            rhs = " ".join(production) if production else "ε"
            action = f"{top} → {rhs}"
            trace.append(action)
            stack.extend(reversed(production))
            steps.append(StackStep(tuple(reversed(stack)), tuple(tokens[cursor:]), action))
        elif top == lookahead:
            action = f"match {top}"
            trace.append(action)
            cursor += 1
            steps.append(StackStep(tuple(reversed(stack)), tuple(tokens[cursor:]), action))
        else:
            error = f"Expected {top}, found {lookahead}"
            steps.append(StackStep(tuple(reversed(stack + [top])), tuple(tokens[cursor:]), f"reject: {error}"))
            return ParseResult(False, tuple(trace), error, tuple(steps))
    if cursor != len(tokens):
        return ParseResult(False, tuple(trace), "Input was not fully consumed", tuple(steps))
    return ParseResult(True, tuple(trace), steps=tuple(steps))

