# CFG and PDA Case Studies

An individual, dependency-free Python project for arithmetic expressions, a restricted assignment-statement syntax, and balanced parentheses. It includes a predictive stack parser, a reusable nondeterministic PDA simulator, CFG-to-PDA construction, FIRST/FOLLOW and LL(1) analysis, ambiguity evidence, and a standalone browser demo.

## Scope

The topics and report criteria are based on the referenced conversation. Its attachments were student reports; the faculty assignment PDF itself was not attached. Check the final scope against your course brief. This implementation is independently written and uses the other report only as context.

## Run

Requires Python 3.10 or newer.

```bash
python -m task3
```

Choose a case from the CLI. Open [`docs/index.html`](docs/index.html) locally for the interactive browser demo. Run the standard-library tests with:

```bash
python -m unittest discover -s tests -v
```

## Case studies and models

| Case | Formal model | What the demo shows |
|---|---|---|
| Arithmetic expressions | LL(1) CFG and deterministic predictive PDA, plus a generic CFG-to-NPDA construction | Precedence, instantaneous descriptions, CFG-to-PDA stack trace, and ambiguity comparison |
| Assignment syntax | `S → id = E` with the expression grammar reused for `E` | Valid and malformed statements parsed through the same PDA stack |
| Balanced parentheses | `S → ( S ) S | ε` and a one-type DPDA | Every push/pop, underflow rejection, and empty-stack acceptance |

The grammar gives `*` higher precedence than `+`; both operators associate left. The ambiguity menu separately shows why `E → E+E | E*E | (E) | id` needs precedence rules: `a+b*c` has two groupings under that grammar.

See [`docs/design.md`](docs/design.md) for CFG productions, the PDA model, an instantaneous-description table, test vectors, Mermaid diagrams, ambiguity witness, limitations, and report-ready content. The same document is the individual report draft.

The CLI includes separate demonstrations for the generic CFG-to-PDA conversion and computed FIRST/FOLLOW sets with the LL(1) parse table. The generic PDA uses breadth-first exploration, returns an accepting configuration path, and stops safely at a fixed configuration bound to avoid unbounded exploration.

## Project layout

```text
task3/grammar.py      CFG representation, FIRST/FOLLOW, LL(1) table and conflict analysis
task3/pda.py          generic PDA simulator, CFG-to-PDA construction, parentheses DPDA
task3/parser.py       tokenizer and predictive PDA stack parser
task3/ambiguity.py    bounded parse-tree witness for an ambiguous CFG
task3/balanced.py     stack recognizer with push/pop trace
task3/__main__.py     interactive terminal demo
tests/                standard-library parser and formal-model cases
docs/design.md        formal design, analysis, diagrams and report content
docs/grammars.json    machine-readable CFG/PDA summary
docs/index.html       standalone interactive browser demonstration
```

## Scope limits

The grammar validates syntax only. It does not evaluate arithmetic, check variable declarations, or implement a complete programming language. It handles identifiers, integer literals, `+`, `*`, and parentheses; the parentheses case study recognizes one delimiter type.

See [`docs/design.md`](docs/design.md) for formal grammar, PDA trace, diagrams, examples, limitations, and report-ready content.

Repository: https://github.com/Saffhrin/FLA-Task3-CFG-PDA
