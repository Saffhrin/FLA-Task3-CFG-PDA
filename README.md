# Task 3 — CFG and PDA Case Studies

An individual, dependency-free Python project demonstrating grammar-based arithmetic expression parsing, restricted assignment syntax checking, and a stack automaton for balanced parentheses.

## Scope

The topics and report criteria are based on the referenced conversation. Its attachments were student reports; the faculty assignment PDF itself was not attached. Check the final scope against your course brief. This implementation is independently written and uses the other report only as context.

## Run

Requires Python 3.10 or newer.

```bash
python -m task3
```

Run the standard-library tests:

```bash
python -m unittest discover -s tests -v
```

## What the models demonstrate

* Arithmetic expressions use an unambiguous LL(1) CFG with multiplication precedence and left associativity. A deterministic PDA simulation uses a predictive parsing stack.
* Assignment statements use `statement → id = expression`, parsed by the same stack machine after the assignment prefix.
* Balanced parentheses use a DPDA-style stack: push `(`, pop `)`, reject underflow or other symbols, and accept at end when the stack is empty.

The grammar validates syntax only. It does not calculate expression values, check variable declarations, or implement a complete programming language.

## Publish later

This folder is already a separate local Git repository. After creating an empty GitHub repository, add it as `origin`, commit the files, and push the `main` branch. No GitHub account was accessed and nothing has been published.

See [`docs/design.md`](docs/design.md) for formal grammar, PDA trace, diagrams, examples, limitations, and report-ready content.
