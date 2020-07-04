from tk_mvc import WindowPart
from tk_mvc import Event
from gui.widgets.hex_cells import HexCells


class SpreadsheetArea(WindowPart):
    def _build(self):
        spreadsheet = HexCells(self,
                               hex_rows=20, hex_columns=20,
                               select_command=self._select_cell,
                               resize_row_command=self._resize_row,
                               resize_column_command=self._resize_column
                               )
        spreadsheet.pack(fill='both', expand=True)

        self._view.add_observer('cell_values', spreadsheet.set_cell_values)
        self._view.add_observer('cell_formats', spreadsheet.set_cell_formats)
        self._view.add_observer('row_sizes', spreadsheet.set_row_sizes)
        self._view.add_observer('column_sizes', spreadsheet.set_column_sizes)

    def _select_cell(self, address):
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
