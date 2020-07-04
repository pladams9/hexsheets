from tk_mvc import WindowPart
from tk_mvc import Event
from gui.widgets.hex_cells import HexCells


class SpreadsheetArea(WindowPart):
    def _build(self):
        self.spreadsheet = HexCells(self,
                               hex_rows=20, hex_columns=20,
                               select_command=self._select_cell,
                               resize_row_command=self._resize_row,
                               resize_column_command=self._resize_column
                               )
        self.spreadsheet.pack(fill='both', expand=True)
        self.spreadsheet.bind('<KeyPress>', self._keypress)

        self._view.add_observer('selected_cell', self.spreadsheet.select_cell)
        self._view.add_observer('cell_values', self.spreadsheet.set_cell_values)
        self._view.add_observer('cell_formats', self.spreadsheet.set_cell_formats)
        self._view.add_observer('row_sizes', self.spreadsheet.set_row_sizes)
        self._view.add_observer('column_sizes', self.spreadsheet.set_column_sizes)
        self._view.add_observer('editing_mode', self._change_edit_mode)

    def _select_cell(self, address):
        if address:
            self._view.add_event(Event('CellSelected', {'address': address}))

    def _resize_row(self, row, height):
        self._view.add_event(Event('RowResized', {
            'row': row,
            'height': height
        }))

    def _resize_column(self, column, width):
        self._view.add_event(Event('ColumnResized', {
            'column': column,
            'width': width
        }))

    def _keypress(self, e):
        events = {
            'Up': Event('CellNavigation', data={'direction': 'up'}),
            'Down': Event('CellNavigation', data={'direction': 'down'}),
            'Left': Event('CellNavigation', data={'direction': 'left'}),
            'Right': Event('CellNavigation', data={'direction': 'right'}),
            'Return': Event('EnterEditMode')
        }
        if e.keysym in events:
            self._view.add_event(events[e.keysym])

    def _change_edit_mode(self, edit_mode):
        if not edit_mode:
            self.spreadsheet.focus_set()
