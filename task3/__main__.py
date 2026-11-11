from .balanced import check_parentheses
from .ambiguity import ambiguous_parse_trees, render_tree
from .grammar import EXPRESSION_GRAMMAR, GRAMMAR_ANALYSIS
from .pda import cfg_to_pda
from .parser import parse, tokenize


def main() -> None:
    while True:
        print("\nCFG / PDA Case Studies\n1) Arithmetic expression\n2) Assignment statement\n3) Balanced parentheses\n4) Ambiguity witness\n5) Construct and run CFG → PDA\n6) FIRST/FOLLOW and LL(1) analysis\nq) Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            return
        if choice not in {"1", "2", "3", "4", "5", "6"}:
            print("Choose 1–6 or q.")
            continue
        if choice == "6":
            for nonterminal in sorted(EXPRESSION_GRAMMAR.nonterminals):
                first = ", ".join(sorted(GRAMMAR_ANALYSIS.first[nonterminal]))
                follow = ", ".join(sorted(GRAMMAR_ANALYSIS.follow[nonterminal]))
                print(f"FIRST({nonterminal}) = {{{first}}}; FOLLOW({nonterminal}) = {{{follow}}}")
            print("LL(1) table conflicts:", dict(GRAMMAR_ANALYSIS.conflicts) or "none")
            continue
        value = input("Input: ")
        if choice == "4":
            try:
                trees = ambiguous_parse_trees(value)
            except ValueError as exc:
                print(f"Invalid expression: {exc}")
                continue
            if not trees:
                print("No parse tree for this input under the ambiguous grammar.")
                continue
            print(f"Ambiguous grammar produced {len(trees)} parse tree(s).")
            for index, tree in enumerate(trees, start=1):
                print(f"\nTree {index}:\n{render_tree(tree)}")
            print("The deployed expression grammar fixes precedence and has one parse tree.")
            continue
        if choice == "5":
            start = input("Start symbol E (expression) or S (assignment) [E]: ").strip().upper() or "E"
            if start not in {"E", "S"}:
                print("Choose E or S.")
                continue
            try:
                symbols = tokenize(value)
            except ValueError as exc:
                print(f"Tokenization error: {exc}")
                continue
            pda = cfg_to_pda(EXPRESSION_GRAMMAR.productions, start, EXPRESSION_GRAMMAR.terminals)
            result = pda.run(symbols)
            status = "ACCEPTED" if result.accepted else "REJECTED"
            if result.limit_reached:
                status = "UNKNOWN (configuration limit reached)"
            print(f"{status}; explored {result.explored_configurations} configurations; standard CFG→PDA is deterministic: {pda.is_deterministic}")
            for step in result.steps:
                config = step.configuration
                remaining = symbols[config.input_index:]
                print(f"  state={config.state}; remaining={remaining!r}; stack(top→bottom)={tuple(reversed(config.stack))!r}; {step.action}")
            continue
        if choice == "3":
            accepted, trace = check_parentheses(value)
            print("ACCEPTED" if accepted else "REJECTED")
            for line in trace:
                print("  " + line)
        else:
            result = parse(value, assignment=choice == "2")
            print("ACCEPTED" if result.accepted else f"REJECTED: {result.error}")
            for step in result.steps:
                print(f"  stack(top→bottom)={list(step.stack_top_first)!r}  input={list(step.input_remaining)!r}  {step.action}")


if __name__ == "__main__":
    main()
