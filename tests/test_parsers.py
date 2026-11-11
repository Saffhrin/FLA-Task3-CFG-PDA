import unittest

from task3.balanced import check_parentheses
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


if __name__ == "__main__":
    unittest.main()
