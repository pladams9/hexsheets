class Model:
    def __init__(self):
        self._cell_formulas = {}
        self._selected_cell = None

    def select_cell(self, x, y):
        self._selected_cell = (x, y)

    def set_selected_cell_formula(self, value):
        if self._selected_cell:
            self._cell_formulas[self._selected_cell] = value

    def get_selected_cell_formula(self):
        if self._selected_cell and (self._selected_cell in self._cell_formulas):
            return self._cell_formulas[self._selected_cell]
        else:
            return ''

    def get_cell_values(self):
        # TODO: change this evaluate formulas
        return self._cell_formulas
