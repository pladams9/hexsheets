import model.formula_parser as fp
import json
import ast


class Model:
    def __init__(self):
        self._cell_formulas = {}
        self._selected_cell = None
        self.editing_cell = False

        self._file_saved = False
        self._file_path = None

    def select_cell(self, x, y):
        self._selected_cell = (x, y)

    def set_selected_cell_formula(self, formula):
        if self._selected_cell:
            self._cell_formulas[self._selected_cell] = formula
            self._file_saved = False

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
        self._file_saved = False
        self._file_path = None

    def open_file(self, filename):
        if filename:
            with open(filename, 'r') as file:
                data = json.load(file)
                self._cell_formulas = {}
                for cell_coord in data:
                    self._cell_formulas[ast.literal_eval(cell_coord)] = data[cell_coord]
                self._file_saved = True
                self._file_path = filename

    def save_file(self, filename='', overwrite=False):
        if (not filename) and overwrite:
            filename = self._file_path

        if filename:
            data = {}
            for cell_coord in self._cell_formulas:
                data[str(cell_coord)] = self._cell_formulas[cell_coord]

            with open(filename, 'w') as file:
                json.dump(data, file)
            self._file_saved = True
            self._file_path = filename

    def get_file_title(self):
        if self._file_path:
            file_title = self._file_path[self._file_path.rfind('/') + 1:]
        else:
            file_title = 'untitled.hxs'
        file_title = '[' + file_title + ']'
        if not self._file_saved:
            file_title += '*'
        return file_title

    def save_file_exists(self):
        if self._file_path:
            return True
        else:
            return False
