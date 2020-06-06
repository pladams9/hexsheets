import tkinter as tk
from tkinter import font


class HexCells(tk.Frame):
    def __init__(self, master, **kwargs):
        self._hex_width = 30
        self._hex_height = 40
        self._hex_columns = 20
        self._hex_rows = 20
        self._canvas_ready = False
        self._cell_coords = {}
        self.current_cell = None
        self._internal_cell_selection = None
        self._select_command = None

        super().__init__(master, **(self._custom_options(**kwargs)))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Colors
        self.colors = {
            'bg': '#BBB',
            'cell-bg': '#EEE',
            'cell-line': '#888',
            'active-cell-line': '#555'
        }

        # Canvas
        self._canvas = tk.Canvas(self)
        self._canvas.config(bg=self.colors['bg'])
        self._canvas.grid(column=0, row=0, sticky='nsew')
        self._canvas.bind('<Button-1>', self._cell_click)
        self._canvas_ready = True
        self._create_hex_grid()

        # Scrollbars
        v_scroll = tk.Scrollbar(self, command=self._canvas.yview)
        v_scroll.grid(column=1, row=0, sticky='nsew')
        h_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self._canvas.xview)
        h_scroll.grid(column=0, row=1, sticky='nsew')
        self._canvas.config(
            xscrollcommand=h_scroll.set,
            yscrollcommand=v_scroll.set
        )

        self.hidden_entry = tk.Entry(self)
        self.hidden_entry.place(x=-100, y=-100)

    def config(self, **kwargs):
        super().config(**(self._custom_options(**kwargs)))

    def _custom_options(self, **kwargs):
        redraw_needed = False
        # Hex Dimensions
        if 'hex_width' in kwargs:
            self._hex_width = kwargs['hex_width']
            kwargs.pop('hex_width')
            redraw_needed = True
        if 'hex_height' in kwargs:
            self._hex_height = kwargs['hex_height']
            kwargs.pop('hex_height')
            redraw_needed = True

        # Rows/Columns
        if 'hex_columns' in kwargs:
            self._hex_columns = kwargs['hex_columns']
            kwargs.pop('hex_columns')
            redraw_needed = True
        if 'hex_rows' in kwargs:
            self._hex_rows = kwargs['hex_rows']
            kwargs.pop('hex_rows')
            redraw_needed = True

        if self._canvas_ready and redraw_needed:
            self._create_hex_grid()

        # Click Command
        if 'select_command' in kwargs:
            self._select_command = kwargs['select_command']
            kwargs.pop('select_command')

        return kwargs

    def _create_hex(self, x, y, width, height):
        hex_coords = [
            x, y,
            x + width, y,
            x + width + (height * 0.25), y + (height / 2),
            x + width, y + height,
            x, y + height,
            x - (height * 0.25), y + (height / 2)
        ]
        hex_shape = self._canvas.create_polygon(hex_coords,
                                                fill=self.colors['cell-bg'],
                                                outline=self.colors['cell-line'],
                                                tag='hex'
                                                )
        return hex_shape

    def _create_cell_text(self, x, y, width, height):
        cell_label = tk.Label(self._canvas, font=font.Font(size=-int(height/3)), anchor=tk.W)
        cell_label.bindtags((str(self._canvas), 'Label', '.', 'all'))

        cell_text = self._canvas.create_window(
            x, y + (height/4),
            anchor=tk.NW, width=width, height=int(height/2),
            window=cell_label, tag='text')

        return cell_text

    def _create_hex_grid(self):
        self._canvas.delete(tk.ALL)
        self._cell_coords = {}
        for cell_y in range(self._hex_rows):
            for cell_x in range(self._hex_columns):
                canvas_x = cell_x * (self._hex_width + (self._hex_height * 0.25))
                canvas_y = (cell_y * self._hex_height) + [0, self._hex_height / 2][cell_x % 2]
                h = self._create_hex(canvas_x, canvas_y,
                                     self._hex_width, self._hex_height)
                self._canvas.addtag_withtag(''.join(['col', str(cell_x)]), h)
                self._canvas.addtag_withtag(''.join(['row', str(cell_y)]), h)
                self._cell_coords[h] = (cell_x, cell_y)

                t = self._create_cell_text(canvas_x, canvas_y, self._hex_width, self._hex_height)
                self._canvas.addtag_withtag(''.join(['col', str(cell_x)]), t)
                self._canvas.addtag_withtag(''.join(['row', str(cell_y)]), t)
        self._canvas.config(scrollregion=self._canvas.bbox(tk.ALL))

    def _cell_click(self, e):
        canvas_x = self._canvas.canvasx(e.widget.winfo_x() + e.x)
        canvas_y = self._canvas.canvasy(e.widget.winfo_y() + e.y)

        self._canvas.dtag('clicked', 'clicked')
        self._canvas.addtag_overlapping('clicked', canvas_x, canvas_y, canvas_x, canvas_y)

        self._canvas.itemconfig('hex', width=1, outline=self.colors['cell-line'])
        matching_cells = self._canvas.find_withtag('clicked && hex')
        if matching_cells:
            cell = matching_cells[0]
            self._canvas.itemconfig(cell, width=2, outline=self.colors['active-cell-line'])
            self._canvas.tag_raise(cell)

            self.current_cell = self._cell_coords[cell]

            if self._select_command:
                self._select_command(self.current_cell)

        self.hidden_entry.focus_set()

    def set_cell_values(self, values):
        items = self._canvas.find_withtag('text&&has_value')
        for item in items:
            cell_label = self.nametowidget(
                self._canvas.itemcget(item, 'window')
            )
            cell_label.config(text='')
        self._canvas.dtag(items, 'has_value')

        for coord in values:
            items = self._canvas.find_withtag('text&&col{0}&&row{1}'.format(coord[0], coord[1]))
            if items:
                cell_label = self.nametowidget(
                    self._canvas.itemcget(items[0], 'window')
                )
                cell_label.config(text=values[coord])
                self._canvas.addtag_withtag('has_value', items[0])


if __name__ == '__main__':
    root = tk.Tk()
    hc = HexCells(root, hex_columns=5, hex_rows=4, relief=tk.SUNKEN, bd=2)
    hc.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    root.mainloop()
