from .balanced import check_parentheses
from .parser import parse


def main() -> None:
    while True:
        print("\nCFG / PDA Case Studies\n1) Arithmetic expression\n2) Assignment statement\n3) Balanced parentheses\nq) Quit")
        choice = input("> ").strip().lower()
        if choice == "q":
            return
        if choice not in {"1", "2", "3"}:
            print("Choose 1, 2, 3, or q.")
            continue
        value = input("Input: ")
        if choice == "3":
            accepted, trace = check_parentheses(value)
            print("ACCEPTED" if accepted else "REJECTED")
            for line in trace:
                print("  " + line)
        else:
            result = parse(value, assignment=choice == "2")
            print("ACCEPTED" if result.accepted else f"REJECTED: {result.error}")
            for move in result.trace:
                print("  " + move)


if __name__ == "__main__":
    main()
