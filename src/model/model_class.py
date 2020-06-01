import model.formula_parser as fp
import json
import ast


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

    def new_file(self):
        self._cell_formulas = {}

    def open_file(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            self._cell_formulas = {}
            for cell_coord in data:
                self._cell_formulas[ast.literal_eval(cell_coord)] = data[cell_coord]

    def save_file(self, filename):
        data = {}
        for cell_coord in self._cell_formulas:
            data[str(cell_coord)] = self._cell_formulas[cell_coord]

        with open(filename, 'w') as file:
            json.dump(data, file)
