import unittest

from pda_cfg.grammar import EXPRESSION_GRAMMAR, analyze
from pda_cfg.pda import balanced_parentheses_pda, cfg_to_pda


class FormalModelTests(unittest.TestCase):
    def test_expression_grammar_is_ll1(self):
        analysis = analyze(EXPRESSION_GRAMMAR)
        self.assertEqual(dict(analysis.conflicts), {})
        self.assertEqual(analysis.first["F"], frozenset({"id", "("}))
        self.assertEqual(analysis.follow["Ep"], frozenset({")", "$"}))

    def test_generic_dpda_accepts_balanced_parentheses(self):
        pda = balanced_parentheses_pda()
        self.assertTrue(pda.is_deterministic)
        self.assertTrue(pda.run(tuple("(()())")).accepted)
        self.assertFalse(pda.run(tuple("(()")).accepted)

    def test_cfg_to_pda_construction_accepts_grammar_strings(self):
        pda = cfg_to_pda(EXPRESSION_GRAMMAR.productions, "E", EXPRESSION_GRAMMAR.terminals)
        self.assertFalse(pda.is_deterministic)
        self.assertTrue(pda.run(("id", "+", "id", "*", "id")).accepted)
        self.assertFalse(pda.run(("id", "+", "*")).accepted)


if __name__ == "__main__":
    unittest.main()
