import model.formula_parser as fp


class Model:
    def __init__(self):
        self._cell_formulas = {}
        self._selected_cell = None
        self.editing_cell = False

    def select_cell(self, x, y):
        self._selected_cell = (x, y)

    def set_selected_cell_formula(self, formula):
        if self._selected_cell:
            self._cell_formulas[self._selected_cell] = formula

    def get_selected_cell_formula(self):
        if self._selected_cell and (self._selected_cell in self._cell_formulas):
            return self._cell_formulas[self._selected_cell]
        else:
            return ''

    def get_cell_values(self):
        parser = fp.FormulaParser()
        parser.update_nodes(self._cell_formulas)
        values = {}
        for cell in self._cell_formulas:
            if cell == self._selected_cell and self.editing_cell:
                values[cell] = self._cell_formulas[cell]
            else:
                values[cell] = parser.get_node_value(cell)
        return values
