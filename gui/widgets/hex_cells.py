import tkinter as tk


class HexCells(tk.Frame):
    def __init__(self, master, **kwargs):
        self._hex_width = 30
        self._hex_height = 40
        self._hex_columns = 20
        self._hex_rows = 20
        self._canvas_ready = False

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

        self.current_cell = None

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
                                                outline=self.colors['cell-line']
                                                )
        self._canvas.tag_bind(hex_shape, '<ButtonPress-1>', lambda e: self._cell_click(hex_shape))
        return hex_shape

    def _create_hex_grid(self):
        self._canvas.delete(tk.ALL)
        for y in range(self._hex_rows):
            for x in range(self._hex_columns):
                h = self._create_hex(x * (self._hex_width + (self._hex_height * 0.25)),
                                     (y * self._hex_height) + [0, self._hex_height / 2][x % 2],
                                     self._hex_width,
                                     self._hex_height)
                self._canvas.addtag_withtag(''.join(['col', str(x)]), h)
                self._canvas.addtag_withtag(''.join(['row', str(y)]), h)
        self._canvas.config(scrollregion=self._canvas.bbox(tk.ALL))

    def _cell_click(self, cell):
        if self.current_cell:
            self._canvas.itemconfig(self.current_cell, width=1, outline=self.colors['cell-line'])
        self.current_cell = cell
        self._canvas.itemconfig(cell, width=2, outline=self.colors['active-cell-line'])
        self._canvas.tag_raise(cell)


if __name__ == '__main__':
    root = tk.Tk()
    hc = HexCells(root, hex_columns=5, hex_rows=4, relief=tk.SUNKEN, bd=2)
    hc.pack(fill=tk.BOTH, padx=10, pady=10)

    root.mainloop()
