import unittest
import core.formula_parser as fp


class TestFormulaParser(unittest.TestCase):
    def setUp(self):
        self.cells_a = {
            (1, 1): 'Test',
            (1, 3): 24,
            (2, 4): '=1+1',
            (3, 1): '=[1, 3] - 2',
            (2, 2): '=[10, 10]',
            (4, 4): '=[5,5]',
            (5, 5): '=[4,4]'
        }
        self.cells_b = {
            (1, 1): 'TEST_2',
            (5, 6): -5
        }
        self.cells_a_plus_b = {
            (1, 1): 'TEST_2',
            (1, 3): 24,
            (2, 4): '=1+1',
            (3, 1): '=[1, 3] - 2',
            (5, 6): -5,
            (2, 2): '=[10, 10]',
            (4, 4): '=[5,5]',
            (5, 5): '=[4,4]'
        }
        self.cells_a_values = {
            (1, 1): 'Test',
            (1, 3): 24,
            (2, 4): 2,
            (3, 1): 22,
            (2, 2): '',
            (4, 4): '#CIRCULAR',
            (5, 5): '#CIRCULAR'
        }
        self.parser = fp.FormulaParser()

    def test_update_nodes(self):
        self.parser.update_nodes(self.cells_a)
        self.assertEqual(self.parser._nodes.keys(), self.cells_a.keys())
        for cell in self.cells_a:
            self.assertEqual(self.parser._nodes[cell], str(self.cells_a[cell]))

        self.parser.update_nodes(self.cells_b)
        self.assertEqual(self.parser._nodes.keys(), self.cells_a_plus_b.keys())
        for cell in self.cells_a_plus_b:
            self.assertEqual(self.parser._nodes[cell], str(self.cells_a_plus_b[cell]))

    def test_clear_nodes(self):
        self.parser.update_nodes(self.cells_a)
        self.parser.clear_nodes()
        self.assertEqual(self.parser._nodes, {})

    def test_get_node_value(self):
        self.parser.update_nodes(self.cells_a)
        for cell in self.cells_a:
            with self.subTest(cell=cell, formula=self.cells_a[cell]):
                self.assertEqual(self.parser.get_node_value(cell), self.cells_a_values[cell])

    def test_cast_value(self):
        values = {
            'test': 'test',
            '1': int(1),
            '1.234': float(1.234),
            '0': int(0),
            '1.0': float(1.0),
            '-0': int(0),
            '-1.678': float(-1.678),
            'A123': 'A123',
            '12.34.56': '12.34.56'
        }
        for value in values:
            with self.subTest(string_value=value, type=type(values[value])):
                self.assertEqual(self.parser._cast_value(value), values[value])
                self.assertIsInstance(self.parser._cast_value(value), type(values[value]))

    def test_tokenize(self):
        strings = {
            '': [],
            'abc': [('VALUE', 'abc')],
            '1 + 2': [('VALUE', '1'), ('OPERATOR', '+'), ('VALUE', '2')],
            '1+2': [('VALUE', '1'), ('OPERATOR', '+'), ('VALUE', '2')],
            '1 + 2 + 3': [('VALUE', '1'), ('OPERATOR', '+'), ('VALUE', '2'), ('OPERATOR', '+'), ('VALUE', '3')],
            '2.5 - 1': [('VALUE', '2.5'), ('OPERATOR', '-'), ('VALUE', '1')],
            '2 + -1': [('VALUE', '2'), ('OPERATOR', '+'), ('OPERATOR', '-'), ('VALUE', '1')],
            '"1 + 2"': [('BRACKET', '"', '1 + 2')],
            '(1 * 2)': [('BRACKET', '(', '1 * 2')],
            '[1, 2]': [('BRACKET', '[', '1, 2')],
            '1* 2': [('VALUE', '1'), ('OPERATOR', '*'), ('VALUE', '2')],
            '1 /2': [('VALUE', '1'), ('OPERATOR', '/'), ('VALUE', '2')]
        }
        for string in strings:
            with self.subTest(string=string):
                self.assertEqual(self.parser._tokenize(string), strings[string])

    def test_parse_formula(self):
        self.parser.update_nodes(self.cells_a)
        formulas = {
            '1+1': 2,
            '1 + 1': 2,
            '[1,3]': 24,
            '[1, 3]': 24,
            '+ 10': '#ERROR',
            '"Cool" + "Neat"': 'CoolNeat',
            '1 + "Test"': '1Test',
            '"Cool" + 2': 'Cool2',
            '1 / "Test"': '#ERROR',
            'Text + 1': 'Text1',
            '"T+xt" + 1': 'T+xt1'
        }
        for formula in formulas:
            with self.subTest(formula=formula):
                self.assertEqual(self.parser._parse_formula(formula), formulas[formula])

    def test_parse_address(self):
        addresses = {
            '1,1': (1, 1),
            '1, 1': (1, 1),
            '-1, -1': (-1, -1),
            '1, -5': (-1, -1),
            '1.5, 1': (-1, -1),
            '1 + 1, 1': (2, 1),
            '1': (-1, -1),
            '1, 1, 1': (-1, -1),
            '1, ': (-1, -1)
        }
        for address in addresses:
            with self.subTest(address=address):
                self.assertEqual(self.parser._parse_address(address), addresses[address])


if __name__ == '__main__':
    unittest.main()
