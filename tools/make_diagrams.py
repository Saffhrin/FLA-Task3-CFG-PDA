"""Generate original Task 3 PDA and parse-tree SVGs using only Python stdlib."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "diagrams"


def start_svg(title, width, height, description):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(description)}">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#344054"/></marker></defs>',
        '<rect width="100%" height="100%" rx="16" fill="#fff"/>',
        '<style>text{font-family:system-ui,Segoe UI,sans-serif;fill:#172b4d}.edge{stroke:#344054;stroke-width:2;fill:none;marker-end:url(#arrow)}.state{fill:#fff;stroke:#344054;stroke-width:2}.nt{fill:#eff4ff;stroke:#84adff;stroke-width:1.5}.term{fill:#f9fafb;stroke:#98a2b3;stroke-width:1.5}.note{font-size:14px;fill:#526174}</style>',
        f'<text x="28" y="36" font-size="21" font-weight="700">{escape(title)}</text>',
    ]


def node(parts, x, y, label, kind="state", radius=38):
    parts.append(f'<circle class="{kind}" cx="{x}" cy="{y}" r="{radius}"/>')
    parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="17">{escape(label)}</text>')


def transition(parts, path, label, x, y, width=270, anchor="middle"):
    parts.append(f'<path class="edge" d="{path}"/>')
    parts.append(f'<rect x="{x-width/2 if anchor=="middle" else x-5}" y="{y-19}" width="{width}" height="48" rx="7" fill="#fff" opacity=".96"/>')
    parts.append(f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="14">')
    for i, line in enumerate(label.split("\n")):
        parts.append(f'<tspan x="{x}" dy="{0 if i==0 else 18}">{escape(line)}</tspan>')
    parts.append('</text>')


def finish(parts):
    parts.append('</svg>')
    return "\n".join(parts) + "\n"


def balanced_dpda():
    parts = start_svg("One-type balanced-parentheses DPDA", 1100, 470,
                      "Single-state deterministic PDA that pushes opening parentheses and pops matching closers")
    parts.append('<path class="edge" d="M95,250 L490,250"/>')
    # Three distinct self-loops keep the stack actions readable.
    transition(parts, "M525,213 C415,83 685,83 575,213", "read '('\nempty stack: push '('", 550, 88, 250)
    transition(parts, "M510,220 C300,110 300,385 510,280", "read '('\ntop '(': replace by '(('", 210, 213, 260)
    transition(parts, "M590,220 C800,110 800,385 590,280", "read ')'\ntop '(': pop", 890, 213, 190)
    node(parts, 550, 250, "q")
    parts.append("<text class=\"note\" x=\"28\" y=\"425\">Accept at end of input exactly when the working stack is empty. A ')' with no '(' on top has no transition.</text>")
    return finish(parts)


def cfg_to_pda():
    parts = start_svg("Standard CFG-to-NPDA construction", 1100, 470,
                      "One-state nondeterministic PDA that expands grammar variables and matches terminals")
    parts.append('<path class="edge" d="M95,245 L490,245"/>')
    transition(parts, "M520,214 C405,60 695,60 580,214", "ε, A → push α\nfor each production A → α", 550, 72, 290)
    transition(parts, "M510,280 C300,410 300,125 510,220", "a, a → ε\nmatch terminal a", 205, 215, 205)
    transition(parts, "M590,280 C800,410 800,125 590,220", "Nondeterministic\nproduction choice", 895, 215, 230)
    node(parts, 550, 250, "q")
    parts.append('<text class="note" x="28" y="425">Start with grammar start variable on stack. Accept when all input is read and the stack is empty.</text>')
    return finish(parts)


def predictive_pda():
    parts = start_svg("LL(1) predictive parser as a deterministic PDA", 1100, 470,
                      "Predictive parser uses one lookahead token and a grammar stack")
    parts.append('<path class="edge" d="M95,245 L490,245"/>')
    transition(parts, "M520,214 C405,60 695,60 580,214", "top is nonterminal A\nuse LL(1) table[A, lookahead]", 550, 70, 285)
    transition(parts, "M510,280 C300,410 300,125 510,220", "top terminal matches\nconsume input and stack top", 205, 215, 255)
    transition(parts, "M590,280 C800,410 800,125 590,220", "replace A by selected RHS\n(top of stack shown first)", 895, 215, 255)
    node(parts, 550, 250, "q")
    parts.append('<text class="note" x="28" y="425">Accept when the end marker and bottom-of-stack marker are both consumed; a missing table entry rejects.</text>')
    return finish(parts)


def tree_node(parts, x, y, label, kind="nt"):
    width = max(52, len(label) * 18 + 20)
    parts.append(f'<rect class="{kind}" x="{x-width/2}" y="{y-22}" width="{width}" height="44" rx="10"/>')
    parts.append(f'<text x="{x}" y="{y+1}" text-anchor="middle" dominant-baseline="middle" font-size="18">{escape(label)}</text>')


def tree_edge(parts, x1, y1, x2, y2):
    parts.append(f'<path d="M{x1},{y1+22} L{x2},{y2-22}" stroke="#667085" stroke-width="1.7"/>')


def ambiguity_trees():
    parts = start_svg("Ambiguous grammar: two trees for id + id * id", 1200, 440,
                      "Two distinct parse trees for the same arithmetic token string")
    parts.append('<text x="300" y="80" text-anchor="middle" font-size="18" font-weight="650">Tree 1: id + (id * id)</text>')
    parts.append('<text x="900" y="80" text-anchor="middle" font-size="18" font-weight="650">Tree 2: (id + id) * id</text>')
    # First parse tree, root plus.
    tree_edge(parts, 300, 140, 180, 230); tree_edge(parts, 300, 140, 420, 230)
    tree_edge(parts, 420, 275, 360, 350); tree_edge(parts, 420, 275, 485, 350)
    tree_edge(parts, 180, 275, 180, 350)
    for x,y,label,kind in [(300,140,"+","nt"),(180,250,"id","term"),(420,250,"*","nt"),(360,370,"id","term"),(485,370,"id","term")]: tree_node(parts,x,y,label,kind)
    # Second parse tree, root multiplication.
    tree_edge(parts, 900, 140, 780, 230); tree_edge(parts, 900, 140, 1020, 230)
    tree_edge(parts, 780, 275, 720, 350); tree_edge(parts, 780, 275, 840, 350)
    tree_edge(parts, 1020, 275, 1020, 350)
    for x,y,label,kind in [(900,140,"*","nt"),(780,250,"+","nt"),(1020,250,"id","term"),(720,370,"id","term"),(840,370,"id","term")]: tree_node(parts,x,y,label,kind)
    return finish(parts)


def precedence_tree():
    parts = start_svg("Precedence grammar: the selected parse tree", 780, 410,
                      "Unambiguous parse tree for id plus id times id, with multiplication nested under addition")
    parts.append('<text class="note" x="28" y="390">The LL(1) grammar admits id + (id * id): multiplication binds more tightly.</text>')
    tree_edge(parts,390,110,250,205); tree_edge(parts,390,110,530,205)
    tree_edge(parts,530,250,465,315); tree_edge(parts,530,250,595,315)
    for x,y,label,kind in [(390,110,"+","nt"),(250,225,"id","term"),(530,225,"*","nt"),(465,340,"id","term"),(595,340,"id","term")]: tree_node(parts,x,y,label,kind)
    return finish(parts)


def assignment_flow():
    parts = start_svg("Assignment syntax case study", 1050, 300,
                      "Assignment grammar uses an identifier, equals sign, and the arithmetic expression grammar")
    labels=[("S",100),("id",305),("=",510),("E",715),("accept",930)]
    for (label,x),(next_label,nx) in zip(labels,labels[1:]):
        left_width=max(52,len(label)*18+20)
        right_width=max(52,len(next_label)*18+20)
        parts.append(f'<path class="edge" d="M{x+left_width/2+5},150 L{nx-right_width/2-5},150"/>')
    for label,x in labels:
        kind="term" if label in {"id","="} else "nt"
        tree_node(parts,x,150,label,kind)
    parts.append('<text class="note" x="28" y="235">Production S → id = E; E is parsed by the same LL(1) expression PDA.</text>')
    parts.append('<text class="note" x="28" y="260">The full input must be consumed. Examples: total=(a+b)*c ✓   a=b+ ✗</text>')
    return finish(parts)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    diagrams={
        "balanced_parentheses_dpda.svg": balanced_dpda(),
        "cfg_to_pda.svg": cfg_to_pda(),
        "predictive_pda.svg": predictive_pda(),
        "expression_ambiguity.svg": ambiguity_trees(),
        "expression_precedence.svg": precedence_tree(),
        "assignment_syntax.svg": assignment_flow(),
    }
    descriptions={
        "balanced_parentheses_dpda.svg":"Push and pop transitions for balanced parentheses; acceptance is by empty stack.",
        "cfg_to_pda.svg":"The standard one-state nondeterministic construction from a CFG to a PDA.",
        "predictive_pda.svg":"The deterministic LL(1) parser expands nonterminals and matches terminals using a stack.",
        "expression_ambiguity.svg":"Two distinct parse trees show ambiguity in the unprioritized expression grammar.",
        "expression_precedence.svg":"The implemented precedence grammar gives multiplication priority over addition.",
        "assignment_syntax.svg":"Assignment syntax begins with an identifier and equals sign, then parses an expression.",
    }
    for filename, svg in diagrams.items():
        (OUT/filename).write_text(svg,encoding="utf-8")
    cards=[]
    for filename, description in descriptions.items():
        title=filename.removesuffix(".svg").replace("_"," ").title()
        cards.append('<article class="card">'+f'<h2>{escape(title)}</h2><p>{escape(description)}</p><a href="{escape(filename)}"><img src="{escape(filename)}" alt="{escape(title)} diagram"></a>'+'</article>')
    template=(ROOT/"tools"/"demo_template.html").read_text(encoding="utf-8")
    (OUT/"index.html").write_text(template.replace("{{DIAGRAM_CARDS}}","\n".join(cards)),encoding="utf-8")
    print(f"Wrote {len(diagrams)} SVG diagrams and {OUT/'index.html'}")


if __name__ == "__main__":
    build()
