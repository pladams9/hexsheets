import tk_mvc
from gui.windows import MainWindow
import core


class Controller(tk_mvc.BaseController):
    def __init__(self):
        super().__init__()

        self.model = core.HexSheetsCore()

        self._view.add_window('MainWindow', MainWindow)
        self._view.show_window('MainWindow')

        self._add_event_handlers({
            'FormulaChanged': self._formula_changed,
            'CellSelected': self._cell_selected,
            'RowResized': self._row_resized,
            'ColumnResized': self._column_resized,
            'NewFile': self._new_file,
            'OpenFile': self._open_file,
            'SaveFile': self._save_file,
            'SaveFileAs': self._save_file_as,
            'ToggleBold': self._toggle_bold,
            'SetCellColor': self._set_cell_color,
            'SetFontColor': self._set_font_color,
            'SetFontSize': self._set_font_size
        })

        self._view.set_value('title', self.model.get_file_title())
        self._new_file()

    def _formula_changed(self, e):
        self.model.set_selected_cell_formula(e.data['formula'])
        self.model.editing_cell = True
        self._view.set_value('cell_values', self.model.get_cell_values())
        self._view.set_value('title', self.model.get_file_title())

    def _cell_selected(self, e):
        xy = e.data['address']
        self.model.select_cell(xy[0], xy[1])

        if self.model.editing_cell:
            self._view.set_value('cell_values', self.model.get_cell_values())
            self.model.editing_cell = False

        self._view.set_value('formula_box', self.model.get_selected_cell_formula())
        self._view.set_value('status_bar', str(xy))

        self._view.set_value('current_cell_color', self.model.get_current_cell_color())
        self._view.set_value('current_cell_font_color', self.model.get_current_cell_font_color())
        self._view.set_value('current_cell_font_size', self.model.get_current_cell_font_size())

    def _row_resized(self, e):
        self.model.set_row_size(e.data['row'], e.data['height'])

    def _column_resized(self, e):
        self.model.set_column_size(e.data['column'], e.data['width'])

    def _new_file(self, e=None):
        self.model.new_file()
        self._view.set_value('cell_values', self.model.get_cell_values())
        self._view.set_value('cell_formats', self.model.get_cell_formats())
        self._view.set_value('current_cell_color', self.model.get_current_cell_color())
        self._view.set_value('current_cell_font_color', self.model.get_current_cell_font_color())
        self._view.set_value('current_cell_font_size', self.model.get_current_cell_font_size())
        self._view.set_value('row_sizes', self.model.get_row_sizes())
        self._view.set_value('column_sizes', self.model.get_column_sizes())
        self._view.set_value('title', self.model.get_file_title())
        self._view.set_value('save_option', self.model.save_file_exists())

    def _open_file(self, e):
        self.model.open_file(e.data['filename'])
        self._view.set_value('row_sizes', self.model.get_row_sizes())
        self._view.set_value('column_sizes', self.model.get_column_sizes())
        self._view.set_value('cell_values', self.model.get_cell_values())
        self._view.set_value('cell_formats', self.model.get_cell_formats())
        self._view.set_value('title', self.model.get_file_title())
        self._view.set_value('save_option', self.model.save_file_exists())

    def _save_file_as(self, e):
        self.model.save_file(filename=e.data['filename'])
        self._view.set_value('title', self.model.get_file_title())
        self._view.set_value('save_option', self.model.save_file_exists())

    def _save_file(self, e):
        self.model.save_file(overwrite=True)
        self._view.set_value('title', self.model.get_file_title())

    def _toggle_bold(self, e):
        self.model.toggle_bold()
        self._view.set_value('cell_formats', self.model.get_cell_formats())

    def _set_cell_color(self, e):
        self.model.set_cell_color(e.data['color'])
        self._view.set_value('current_cell_color', e.data['color'])
        self._view.set_value('cell_formats', self.model.get_cell_formats())

    def _set_font_color(self, e):
        self.model.set_cell_font_color(e.data['color'])
        self._view.set_value('current_cell_font_color', e.data['color'])
        self._view.set_value('cell_formats', self.model.get_cell_formats())

    def _set_font_size(self, e):
        self.model.set_cell_font_size(e.data['font_size'])
        self._view.set_value('cell_formats', self.model.get_cell_formats())
