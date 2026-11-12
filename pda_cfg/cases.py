"""Case-study descriptions and example strings used in the report and CLI."""

CASE_EXAMPLES = {
    "Arithmetic expressions": {
        "accepted": ("a+b", "a*b", "(a+b)*c", "x1 + 23 * y", "a*(b+c)+d"),
        "rejected": ("a+", "*ab", "(a+b", "a b", "a++b"),
        "grammar": "E -> T E'; E' -> + T E' | ε; T -> F T'; T' -> * F T' | ε; F -> ( E ) | id",
    },
    "Assignment syntax": {
        "accepted": ("a=b", "a=b+c", "x=y*z", "total=(a+b)*c", "result = value1 + 42"),
        "rejected": ("=a+b", "a=b+", "a==b", "a+b=c", "a=b; c=d"),
        "grammar": "S -> id = E, where E is the arithmetic-expression grammar",
    },
    "Balanced parentheses": {
        "accepted": ("ε (empty)", "()", "(())", "()()", "(()())"),
        "rejected": ("(", "(()", ")(", "())", "(a)"),
        "grammar": "S -> ( S ) S | ε",
    },
}
