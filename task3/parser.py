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
class ParseResult:
    accepted: bool
    trace: tuple[str, ...]
    error: str | None = None


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
    while stack:
        top = stack.pop()
        lookahead = tokens[cursor]
        if top in NONTERMINALS:
            production = TABLE.get((top, lookahead))
            if production is None:
                return ParseResult(False, tuple(trace), f"No production for {top} with lookahead {lookahead}")
            rhs = " ".join(production) if production else "ε"
            trace.append(f"{top} → {rhs}")
            stack.extend(reversed(production))
        elif top == lookahead:
            trace.append(f"match {top}")
            cursor += 1
        else:
            return ParseResult(False, tuple(trace), f"Expected {top}, found {lookahead}")
    if cursor != len(tokens):
        return ParseResult(False, tuple(trace), "Input was not fully consumed")
    return ParseResult(True, tuple(trace))
