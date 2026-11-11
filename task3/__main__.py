from .balanced import check_parentheses
from .ambiguity import ambiguous_parse_trees, render_tree
from .parser import parse


def main() -> None:
    while True:
        print("\nCFG / PDA Case Studies\n1) Arithmetic expression\n2) Assignment statement\n3) Balanced parentheses\n4) Ambiguity witness\nq) Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            return
        if choice not in {"1", "2", "3"}:
            print("Choose 1, 2, 3, or q.")
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

