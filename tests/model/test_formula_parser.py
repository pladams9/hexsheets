import unittest
import model.formula_parser as fp


class TestFormulaParser(unittest.TestCase):
    def setUp(self):
        self.cells_a = {
            (1, 1): 'Test',
            (1, 3): 24,
            (2, 4): '=1+1',
            (3, 1): '=[1, 3] - 2'
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
            (5, 6): -5
        }
        self.delete_cells = [
            (1, 1),
            (1, 3)
        ]
        self.cells_a_minus_delete = {
            (2, 4): '=1+1',
            (3, 1): '=[1, 3] - 2'
        }
        self.cells_a_values = {
            (1, 1): 'Test',
            (1, 3): 24,
            (2, 4): 2,
            (3, 1): 22
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

    def test_delete_nodes(self):
        self.parser.update_nodes(self.cells_a)
        self.parser.delete_nodes(self.delete_cells)
        self.assertEqual(self.parser._nodes.keys(), self.cells_a_minus_delete.keys())
        for cell in self.cells_a_minus_delete:
            self.assertEqual(self.parser._nodes[cell], str(self.cells_a_minus_delete[cell]))

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

if __name__ == '__main__':
    unittest.main()
