import unittest
from itertools import product

from task3.balanced import check_parentheses
from task3.ambiguity import ambiguous_parse_trees
from task3.parser import parse


class GrammarAndPdaTests(unittest.TestCase):
    def test_arithmetic_accepts(self):
        for source in ("a+b", "a*b", "(a+b)*c", "x1 + 23 * y", "a*(b+c)+d"):
            with self.subTest(source=source):
                self.assertTrue(parse(source).accepted)

    def test_arithmetic_rejects(self):
        for source in ("a+", "*ab", "(a+b", "a b", "a++b"):
            with self.subTest(source=source):
                self.assertFalse(parse(source).accepted)

    def test_assignment_accepts(self):
        for source in ("a=b", "a=b+c", "x=y*z", "total=(a+b)*c", "result = value1 + 42"):
            with self.subTest(source=source):
                self.assertTrue(parse(source, assignment=True).accepted)

    def test_assignment_rejects(self):
        for source in ("=a+b", "a=b+", "a==b", "a+b=c", "a=b; c=d"):
            with self.subTest(source=source):
                self.assertFalse(parse(source, assignment=True).accepted)

    def test_parentheses_accepts(self):
        for source in ("", "()", "(())", "()()", "(()())"):
            with self.subTest(source=source):
                self.assertTrue(check_parentheses(source)[0])

    def test_parentheses_rejects(self):
        for source in ("(", "(()", ")(", "())", "(a)"):
            with self.subTest(source=source):
                self.assertFalse(check_parentheses(source)[0])

    def test_ambiguity_witness_has_two_trees(self):
        self.assertEqual(len(ambiguous_parse_trees("a+b*c")), 2)

    def test_predictive_pda_trace_records_configurations(self):
        result = parse("a+b")
        self.assertTrue(result.accepted)
        self.assertTrue(result.steps)
        self.assertIn("$", result.steps[-1].action)

    def test_parenthesis_pda_agrees_with_independent_prefix_check(self):
        for size in range(7):
            for symbols in product("()x", repeat=size):
                source = "".join(symbols)
                depth = 0
                expected = True
                for char in source:
                    if char == "(":
                        depth += 1
                    elif char == ")":
                        depth -= 1
                        if depth < 0:
                            expected = False
                            break
                    else:
                        expected = False
                        break
                expected = expected and depth == 0
                with self.subTest(source=source):
                    self.assertEqual(expected, check_parentheses(source)[0])


if __name__ == "__main__":
    unittest.main()

