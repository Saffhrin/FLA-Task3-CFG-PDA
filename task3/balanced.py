"""Stack-based recognizer for the one-type balanced-parentheses language."""


def check_parentheses(source: str) -> tuple[bool, tuple[str, ...]]:
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
    if stack:
        trace.append(f"end: reject ({len(stack)} unmatched opening parenthesis/parentheses)")
        return False, tuple(trace)
    trace.append("end: accept (stack empty)")
    return True, tuple(trace)
