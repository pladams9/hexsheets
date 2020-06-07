import tkinter as tk
from tkinter import font


class HexCells(tk.Frame):
    def __init__(self, master, **kwargs):
        self._default_column_width = 30
        self._default_row_height = 40
        self._point_width = 10
        self._hex_columns = 20
        self._hex_rows = 20

        self._canvas_ready = False

        self._cell_coords = {}
        self.current_cell = None
        self._internal_cell_selection = None
        self._select_command = None

        self._cell_values = {}

        super().__init__(master, **(self._custom_options(**kwargs)))

        # Colors
        self.colors = {
            'bg': '#BBB',
            'cell-bg': '#EEE',
            'cell-line': '#888',
            'active-cell-line': '#555'
        }

        # Row/Column Widgets
        self._column_shelf = tk.Canvas(self, height=20)
        self._column_shelf.grid(column=1, row=0, sticky='nsew')
        self._column_handles = []
        self._column_ids = {}
        self._column_widths = [self._default_column_width for i in range(self._hex_columns)]

        self._row_shelf = tk.Canvas(self, width=20)
        self._row_shelf.grid(column=0, row=1, sticky='nsew')
        self._row_handles = []
        self._row_ids = []
        self._row_heights = [self._default_row_height for i in range(self._hex_rows)]

        self.resizing_id = None
        self.resize_coord = None

        # Canvas
        self._canvas = tk.Canvas(self)
        self._canvas.config(bg=self.colors['bg'])
        self._canvas.grid(column=1, row=1, sticky='nsew')
        self._canvas.bind('<Button-1>', self._cell_click)
        self._canvas_ready = True
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        # Build out canvas
        self._build_canvas_items()

        # Scrollbars
        self._v_scroll = tk.Scrollbar(self)
        self._v_scroll.grid(column=2, row=1, sticky='nsew')
        self._h_scroll = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self._h_scroll.grid(column=1, row=2, sticky='nsew')

        self._canvas.config(
            xscrollcommand=self._h_scroll.set,
            yscrollcommand=self._v_scroll.set
        )

        def y_scroll(*args):
            self._canvas.yview(*args)
            self._row_shelf.yview(*args)
        self._v_scroll.config(command=y_scroll)
        self._canvas.yview_moveto(0)
        self._row_shelf.yview_moveto(0)

        def x_scroll(*args):
            self._canvas.xview(*args)
            self._column_shelf.xview(*args)
        self._h_scroll.config(command=x_scroll)
        self._canvas.xview_moveto(0)
        self._column_shelf.xview_moveto(0)



        # Hidden entry box TODO: Remove this entry box and move entry outside of widget
        self.hidden_entry = tk.Entry(self)
        self.hidden_entry.place(x=-100, y=-100)

    def config(self, **kwargs):
        super().config(**(self._custom_options(**kwargs)))

    def _custom_options(self, **kwargs):
        redraw_needed = False
        # Hex Dimensions
        if 'hex_width' in kwargs:
            self._default_column_width = kwargs['hex_width']
            kwargs.pop('hex_width')
            redraw_needed = True
        if 'hex_height' in kwargs:
            self._default_row_height = kwargs['hex_height']
            self._point_width = self._default_row_height / 4
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
            self._build_canvas_items()

        # Click Command
        if 'select_command' in kwargs:
            self._select_command = kwargs['select_command']
            kwargs.pop('select_command')

        return kwargs

    def _create_hex(self, x, y, width, top_height, bottom_height):
        full_height = top_height + bottom_height
        hex_coords = [
            x, y,
            x + width, y,
            x + width + self._point_width, y + top_height,
            x + width, y + full_height,
            x, y + full_height,
            x - self._point_width, y + top_height
        ]
        hex_shape = self._canvas.create_polygon(hex_coords,
                                                fill=self.colors['cell-bg'],
                                                outline=self.colors['cell-line'],
                                                tag='hex'
                                                )
        return hex_shape

    def _create_cell_text(self, x, y, width, height):
        cell_label = tk.Label(self._canvas, font=font.Font(size=-int(height / 3)), anchor=tk.W)
        cell_label.bindtags((str(self._canvas), 'Label', '.', 'all'))

        cell_text = self._canvas.create_window(
            x, y + (height / 4),
            anchor=tk.NW, width=width, height=int(height / 2),
            window=cell_label, tag='text')

        return cell_text

    def _create_hex_grid(self):
        self._canvas.delete(tk.ALL)
        self._cell_coords = {}

        for cell_y in range(self._hex_rows):
            for cell_x in range(self._hex_columns):
                canvas_x = sum(w + self._point_width for w in self._column_widths[0:cell_x])
                canvas_y = sum(self._row_heights[0:cell_y]) + [0, self._row_heights[cell_y] / 2][cell_x % 2]

                if ((cell_x % 2) != 0) and (cell_y + 1 != self._hex_rows):
                    h = self._create_hex(canvas_x, canvas_y, self._column_widths[cell_x], self._row_heights[cell_y] / 2,
                                         self._row_heights[cell_y + 1] / 2)
                else:
                    h = self._create_hex(canvas_x, canvas_y, self._column_widths[cell_x], self._row_heights[cell_y] / 2,
                                         self._row_heights[cell_y] / 2)

                self._canvas.addtag_withtag(''.join(['col', str(cell_x)]), h)
                self._canvas.addtag_withtag(''.join(['row', str(cell_y)]), h)
                self._cell_coords[h] = (cell_x, cell_y)

                t = self._create_cell_text(canvas_x, canvas_y, self._column_widths[cell_x], self._row_heights[cell_y])
                self._canvas.addtag_withtag(''.join(['col', str(cell_x)]), t)
                self._canvas.addtag_withtag(''.join(['row', str(cell_y)]), t)

        limits = (
            -self._point_width - 1,
            -1,
            sum(self._column_widths) + (self._hex_columns * self._point_width) + 1,
            sum(self._row_heights) + (self._row_heights[-1] / 2) + 1
        )
        self._canvas.config(scrollregion=limits)

    def _create_column_handles(self):
        self._column_shelf.delete(tk.ALL)
        for column in self._column_handles:
            column['handle'].destroy()
            column['sash'].destroy()
        self._column_handles = []
        self._column_ids = {}

        for x in range(self._hex_columns):
            new_column_handle = {
                'handle': tk.Frame(self._column_shelf, relief=tk.RAISED, bd=2),
                'sash': tk.Frame(self._column_shelf, width=self._point_width, bg='#BBB', cursor='sb_h_double_arrow')
            }

            self._column_handles.append(new_column_handle)
            self._column_ids[new_column_handle['sash'].winfo_name()] = x

            self._column_handles[x]['sash'].bind('<Button-1>', self._start_column_resize)
            self._column_handles[x]['sash'].bind('<ButtonRelease-1>', self._finish_column_resize)

            handle = self._column_shelf.create_window(
                sum(self._column_widths[:x]) + (x * self._point_width), 0,
                anchor=tk.NW, width=self._column_widths[x], height=20,
                window=new_column_handle['handle'], tag='col-handle')
            self._column_shelf.addtag_withtag(''.join(['col', str(x)]), handle)

            sash = self._column_shelf.create_window(
                sum(self._column_widths[:(x+1)]) + (x * self._point_width), 0,
                anchor=tk.NW, width=self._point_width, height=20,
                window=new_column_handle['sash'], tag='col-sash')
            self._column_shelf.addtag_withtag(''.join(['col', str(x)]), sash)

        limits = (
            -self._point_width - 1,
            0,
            sum(self._column_widths) + (self._hex_columns * self._point_width),
            20
        )
        self._column_shelf.config(scrollregion=limits)

    def _create_row_handles(self):
        self._row_shelf.delete(tk.ALL)
        for row in self._row_handles:
            row['handle'].destroy()
            row['sash'].destroy()
        self._row_handles = []
        self._row_ids = {}

        for y in range(self._hex_rows):
            new_row_handle = {
                'handle': tk.Frame(self._row_shelf, relief=tk.RAISED, bd=2),
                'sash': tk.Frame(self._row_shelf, bg='#BBB', cursor='sb_v_double_arrow')
            }
            self._row_handles.append(new_row_handle)
            self._row_ids[new_row_handle['sash'].winfo_name()] = y

            self._row_handles[y]['sash'].bind('<Button-1>', self._start_row_resize)
            self._row_handles[y]['sash'].bind('<ButtonRelease-1>', self._finish_row_resize)

            handle = self._row_shelf.create_window(
                0, sum(self._row_heights[:y]) + 2,
                anchor=tk.NW, height=self._row_heights[y]-4, width=20,
                window=new_row_handle['handle'], tag='col-handle')
            self._row_shelf.addtag_withtag(''.join(['col', str(y)]), handle)

            sash = self._row_shelf.create_window(
                0, sum(self._row_heights[:(y+1)]) - 2,
                anchor=tk.NW, height=4, width=20,
                window=new_row_handle['sash'], tag='row-handle')
            self._row_shelf.addtag_withtag(''.join(['col', str(y)]), sash)

        limits = (
            0,
            -2,
            20,
            sum(self._row_heights) + (self._row_heights[-1] / 2) + 4
        )
        self._row_shelf.config(scrollregion=limits)

    def _build_canvas_items(self):
        self._create_hex_grid()
        self._create_column_handles()
        self._create_row_handles()

        self._update_cell_values()

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
        self._cell_values = values
        self._update_cell_values()

    def _update_cell_values(self):
        items = self._canvas.find_withtag('text&&has_value')
        for item in items:
            cell_label = self.nametowidget(
                self._canvas.itemcget(item, 'window')
            )
            cell_label.config(text='')
        self._canvas.dtag(items, 'has_value')

        for coord in self._cell_values:
            items = self._canvas.find_withtag('text&&col{0}&&row{1}'.format(coord[0], coord[1]))
            if items:
                cell_label = self.nametowidget(
                    self._canvas.itemcget(items[0], 'window')
                )
                cell_label.config(text=self._cell_values[coord])
                self._canvas.addtag_withtag('has_value', items[0])

    def _start_column_resize(self, e):
        self.resizing_id = self._column_ids[e.widget.winfo_name()]
        self.resize_coord = e.x

        def update_line():
            self._canvas.delete('resize_line')

            if self.resizing_id is not None:
                x = self._canvas.canvasx(self.winfo_pointerx() - self._canvas.winfo_rootx())

                line = self._canvas.create_line(x, 0, x, 1000)
                self._canvas.addtag_withtag('resize_line', line)

                self.after(33, update_line)

        update_line()

        # TODO: Add line to canvas to visualize resizing

    def _finish_column_resize(self, e):
        if self.resize_coord is not None:
            diff = e.x - self.resize_coord
            width = self._column_widths[self.resizing_id]
            width += diff
            width = max(10, width)
            self._column_widths[self.resizing_id] = width

            self.resize_coord = None
            self.resizing_id = None

            self._build_canvas_items()

    def _start_row_resize(self, e):
        self.resizing_id = self._row_ids[e.widget.winfo_name()]
        self.resize_coord = e.y

        def update_line():
            self._canvas.delete('resize_line')

            if self.resizing_id is not None:
                y = self._canvas.canvasy(self.winfo_pointery() - self._canvas.winfo_rooty())

                # TODO: change line length to match current window

                line = self._canvas.create_line(0, y, 1000, y)
                self._canvas.addtag_withtag('resize_line', line)

                self.after(33, update_line)

        update_line()

    def _finish_row_resize(self, e):
        if self.resize_coord is not None:
            diff = e.y - self.resize_coord
            height = self._row_heights[self.resizing_id]
            height += diff
            height = max(10, height)
            self._row_heights[self.resizing_id] = height

            self.resize_coord = None
            self.resizing_id = None

            self._build_canvas_items()


if __name__ == '__main__':
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    geo_string = str(int(screen_width * 0.7)) + 'x' + str(int(screen_height * 0.7)) + \
        '+' + str(int(screen_width * 0.15)) + '+' + str(int(screen_height * 0.15))
    root.geometry(geo_string)

    hc = HexCells(root, hex_columns=20, hex_rows=20, relief=tk.SUNKEN, bd=2)
    hc.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    hc.set_cell_values({
        (1, 2): 'Test',
        (2, 2): 1,
        (3, 4): 42
    })

    root.mainloop()
