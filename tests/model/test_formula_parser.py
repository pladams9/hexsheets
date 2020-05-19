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
            (5, 6): '=([3,1] * [2,4]) - [1,3]'
        }
        self.delete_cells = []
        self.parser = fp.FormulaParser()

    def test_update_nodes(self):
        self.parser.update_nodes(self.cells_a)
        self.assertEqual(self.parser._nodes.keys(), self.cells_a.keys())
        # TODO: Check value of nodes

        # TODO: Add in cells_b and check resulting nodes

    def test_delete_nodes(self):
        self.parser.update_nodes(self.cells_a)
        self.parser.delete_nodes(self.delete_cells)
        # TODO: Check existence of cells
        # TODO: Check values of nodes

    def test_get_node_value(self):
        self.parser.update_nodes(self.cells_a)
        for cell in self.cells_a:
            # TODO: check value
            pass


if __name__ == '__main__':
    unittest.main()
