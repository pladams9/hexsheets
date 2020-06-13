import tk_mvc
from gui.windows import MainWindow
import model


class Controller(tk_mvc.BaseController):
    def __init__(self):
        super().__init__()

        self.model = model.Model()

        self._view.add_window('MainWindow', MainWindow)
        self._view.show_window('MainWindow')

        self.add_event_handlers({
            'FormulaChanged': self.formula_changed,
            'CellSelected': self.cell_selected,
            'RowResized': self.row_resized,
            'ColumnResized': self.column_resized,
            'NewFile': self.new_file,
            'OpenFile': self.open_file,
            'SaveFile': self.save_file,
            'SaveFileAs': self.save_file_as
        })

        self._view.set_value('title', self.model.get_file_title())
        self.new_file()

    def formula_changed(self, e):
        self.model.set_selected_cell_formula(e.data['formula'])
        self.model.editing_cell = True
        self._view.set_value('cell_values', self.model.get_cell_values())
        self._view.set_value('title', self.model.get_file_title())

    def cell_selected(self, e):
        xy = e.data['address']
        self.model.select_cell(xy[0], xy[1])

        if self.model.editing_cell:
            self._view.set_value('cell_values', self.model.get_cell_values())
            self.model.editing_cell = False

        self._view.set_value('formula_box', self.model.get_selected_cell_formula())
        self._view.set_value('status_bar', str(xy))

    def row_resized(self, e):
        self.model.set_row_size(e.data['row'], e.data['height'])

    def column_resized(self, e):
        self.model.set_column_size(e.data['column'], e.data['width'])

    def new_file(self, e=None):
        self.model.new_file()
        self._view.set_value('cell_values', self.model.get_cell_values())
        self._view.set_value('row_sizes', self.model.get_row_sizes())
        self._view.set_value('column_sizes', self.model.get_column_sizes())
        self._view.set_value('title', self.model.get_file_title())
        self._view.set_value('save_option', self.model.save_file_exists())

    def open_file(self, e):
        self.model.open_file(e.data['filename'])
        self._view.set_value('cell_values', self.model.get_cell_values())
        self._view.set_value('row_sizes', self.model.get_row_sizes())
        self._view.set_value('column_sizes', self.model.get_column_sizes())
        self._view.set_value('title', self.model.get_file_title())
        self._view.set_value('save_option', self.model.save_file_exists())

    def save_file_as(self, e):
        self.model.save_file(filename=e.data['filename'])
        self._view.set_value('title', self.model.get_file_title())
        self._view.set_value('save_option', self.model.save_file_exists())

    def save_file(self, e):
        self.model.save_file(overwrite=True)
        self._view.set_value('title', self.model.get_file_title())
