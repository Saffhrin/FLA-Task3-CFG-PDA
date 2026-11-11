"""Bounded parse-tree witness for the intentionally ambiguous expression CFG."""
from .parser import tokenize

Tree = str | tuple[str, "Tree", "Tree"]


def _outer_parentheses_cover(tokens: list[str]) -> bool:
    if len(tokens) < 2 or tokens[0] != "(" or tokens[-1] != ")":
        return False
    depth = 0
    for i, token in enumerate(tokens):
        depth += token == "("
        depth -= token == ")"
        if depth == 0 and i != len(tokens) - 1:
            return False
    return depth == 0


def ambiguous_parse_trees(source: str, limit: int = 100) -> tuple[Tree, ...]:
    """Enumerate parses for E → E+E | E*E | (E) | id on a bounded input.

    This helper is a teaching witness, separate from the production LL(1)
    parser. It caps output to avoid combinatorial growth on long inputs.
    """
    tokens = tokenize(source)

    def parse_span(part: list[str]) -> list[Tree]:
        if part == ["id"]:
            return ["id"]
        if _outer_parentheses_cover(part):
            return parse_span(part[1:-1])
        depth = 0
        parses: list[Tree] = []
        for i, token in enumerate(part):
            if token == "(":
                depth += 1
            elif token == ")":
                depth -= 1
            elif depth == 0 and token in {"+", "*"}:
                left = parse_span(part[:i])
                right = parse_span(part[i + 1:])
                parses.extend((token, ltree, rtree) for ltree in left for rtree in right)
                if len(parses) >= limit:
                    return parses[:limit]
        return parses

    return tuple(parse_span(tokens))


def render_tree(tree: Tree, indent: str = "") -> str:
    if isinstance(tree, str):
        return indent + tree
    operator, left, right = tree
    return "\n".join((indent + operator, render_tree(left, indent + "  "), render_tree(right, indent + "  ")))

