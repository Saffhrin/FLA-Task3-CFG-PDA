"""One-type balanced-parentheses recognizer backed by the generic PDA engine."""
from .pda import balanced_parentheses_pda

_PDA = balanced_parentheses_pda()


def check_parentheses(source: str) -> tuple[bool, tuple[str, ...]]:
    result = _PDA.run(source)
    if result.accepted:
        trace = tuple(
            f"{step.configuration.input_index}: state={step.configuration.state}; "
            f"remaining={source[step.configuration.input_index:]!r}; "
            f"stack={step.configuration.stack!r}; {step.action}"
            for step in result.steps
        )
        return True, trace

    # Show the first local reason the deterministic run cannot continue.
    stack: list[str] = []
    trace: list[str] = []
    for index, char in enumerate(source):
        if char == "(":
            stack.append("(")
            trace.append(f"{index}: read '(' → push '('; depth={len(stack)}")
        elif char == ")":
            if not stack:
                trace.append(f"{index}: read ')' → reject (stack underflow)")
                return False, tuple(trace)
            stack.pop()
            trace.append(f"{index}: read ')' → pop '('; depth={len(stack)}")
        else:
            trace.append(f"{index}: read {char!r} → reject (outside alphabet)")
            return False, tuple(trace)
    trace.append(f"end: reject ({len(stack)} unmatched opening parenthesis/parentheses)")
    return False, tuple(trace)
