import hexsheets_view
import model


class Controller:
    def __init__(self):
        self.model = model.Model()
        self.view = hexsheets_view.HexSheetsView()

        self._event_handlers = {
            'FormulaChanged': self.formula_changed,
            'CellSelected': self.cell_selected,
            'RowResized': self.row_resized,
            'ColumnResized': self.column_resized,
            'NewFile': self.new_file,
            'OpenFile': self.open_file,
            'SaveFile': self.save_file,
            'SaveFileAs': self.save_file_as
        }

    def start(self):
        self.view.set_value('title', self.model.get_file_title())

        self.new_file()

        self.view.add_loop_hook(self.handle_events, 100)
        self.view.start_mainloop()

    def handle_events(self):
        for e in self.view.get_events():
            if e.type in self._event_handlers:
                self._event_handlers[e.type](e)

    def formula_changed(self, e):
        self.model.set_selected_cell_formula(e.data['formula'])
        self.model.editing_cell = True
        self.view.set_value('cell_values', self.model.get_cell_values())
        self.view.set_value('title', self.model.get_file_title())

    def cell_selected(self, e):
        xy = e.data['address']
        self.model.select_cell(xy[0], xy[1])

        if self.model.editing_cell:
            self.view.set_value('cell_values', self.model.get_cell_values())
            self.model.editing_cell = False

        self.view.set_value('formula_box', self.model.get_selected_cell_formula())
        self.view.set_value('status_bar', str(xy))

    def row_resized(self, e):
        self.model.set_row_size(e.data['row'], e.data['height'])

    def column_resized(self, e):
        self.model.set_column_size(e.data['column'], e.data['width'])

    def new_file(self, e=None):
        self.model.new_file()
        self.view.set_value('cell_values', self.model.get_cell_values())
        self.view.set_value('row_sizes', self.model.get_row_sizes())
        self.view.set_value('column_sizes', self.model.get_column_sizes())
        self.view.set_value('title', self.model.get_file_title())
        self.view.set_value('save_option', self.model.save_file_exists())

    def open_file(self, e):
        self.model.open_file(e.data['filename'])
        self.view.set_value('cell_values', self.model.get_cell_values())
        self.view.set_value('row_sizes', self.model.get_row_sizes())
        self.view.set_value('column_sizes', self.model.get_column_sizes())
        self.view.set_value('title', self.model.get_file_title())
        self.view.set_value('save_option', self.model.save_file_exists())

    def save_file_as(self, e):
        self.model.save_file(filename=e.data['filename'])
        self.view.set_value('title', self.model.get_file_title())
        self.view.set_value('save_option', self.model.save_file_exists())

    def save_file(self, e):
        self.model.save_file(overwrite=True)
        self.view.set_value('title', self.model.get_file_title())
