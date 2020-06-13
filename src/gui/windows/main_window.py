from tk_mvc import BaseWindow
import tkinter as tk
import tkinter.filedialog as fd
import gui.widgets
from tk_mvc import event
import webbrowser
import os


class MainWindow(BaseWindow):
    def __init__(self, view, parent):
        super().__init__(view, parent)

        parent.geometry('800x600')

        self._view.add_observer('title', self.update_title)

        menu_bar = tk.Menu(parent)
        parent.configure(menu=menu_bar)

        self.file_menu = tk.Menu(menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self._new_file)
        self.file_menu.add_command(label="Open...", command=self._open_file)
        self._save_option_allowed = False
        self._view.add_observer('save_option', self.update_save_option)
        self.file_menu.add_command(label="Save", command=self._save_file)
        self.file_menu.add_command(label="Save As...", command=self._save_file_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.quit)
        self._parent_toplevel.protocol("WM_DELETE_WINDOW", self.quit)
        menu_bar.add_cascade(label="File", menu=self.file_menu)

        menu_bar.add_command(label='Help', command=self._help)

        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)
        mainframe = tk.Frame(parent)
        mainframe.grid(sticky='nsew')
        mainframe.rowconfigure(1, weight=1)
        mainframe.columnconfigure(0, weight=1)

        top_bar = tk.Frame(mainframe)
        top_bar.grid(column=0, row=0, sticky='nsew')
        top_bar.columnconfigure(0, weight=1)

        # TODO: Add buttons on the tool bar
        '''
        tool_bar = tk.Frame(top_bar)
        tk.Button(tool_bar, text='Test').pack(side=tk.LEFT)
        tool_bar.grid(column=0, row=0, sticky='we')
        '''

        formula_bar = tk.Frame(top_bar)
        formula_bar.grid(column=0, row=1, sticky='we')
        tk.Label(formula_bar, text='Formula:').pack(side=tk.LEFT)

        self.formula_box = tk.Entry(formula_bar)
        self.formula_box.pack(fill=tk.X)
        self._view.add_observer('formula_box', self.update_formula_box)

        self.spreadsheet = gui.widgets.HexCells(mainframe,
                                                hex_rows=20, hex_columns=20,
                                                select_command=self.select_cell,
                                                resize_row_command=self.resize_row,
                                                resize_column_command=self.resize_column
        )
        self.spreadsheet.grid(column=0, row=1, sticky='nsew')
        self._view.add_observer('cell_values', self.spreadsheet.set_cell_values)
        self._view.add_observer('row_sizes', self.spreadsheet.set_row_sizes)
        self._view.add_observer('column_sizes', self.spreadsheet.set_column_sizes)

        self._formula_boxes = [
            self.formula_box,
            self.spreadsheet.hidden_entry
        ]
        vcmd = (self._parent_toplevel.register(self._enter_formula), '%W', '%P')
        for box in self._formula_boxes:
            box.config(vcmd=vcmd)
            box.bind("<FocusIn>", lambda e: e.widget.config(validate='key'))
            box.bind("<FocusOut>", lambda e: e.widget.config(validate='none'))

        self.status_bar = tk.Label(mainframe, relief=tk.GROOVE, anchor=tk.W)
        self.status_bar.grid(column=0, row=2, sticky=(tk.W, tk.E))
        self._view.add_observer('status_bar', self.update_status_bar)

    def update_status_bar(self, text):
        self.status_bar.config(text=text)

    def update_title(self, text):
        self._parent_toplevel.title('HexSheets - ' + text)

    def _enter_formula(self, widget, new_text):
        for box in self._formula_boxes:
            if box != self._parent_toplevel.nametowidget(widget):
                box.delete(0, tk.END)
                box.insert(0, new_text)
        self._view.add_event(event.Event('FormulaChanged', {'formula': new_text}))

        return True

    def update_formula_box(self, text):
        for box in self._formula_boxes:
            validation = box.cget('validate')
            box.config(validate='none')
            box.delete(0, tk.END)
            box.insert(0, text)
            box.config(validate=validation)

    def select_cell(self, address):
        self._view.add_event(event.Event('CellSelected', {'address': address}))

    def resize_row(self, row, height):
        self._view.add_event(event.Event('RowResized', {
            'row': row,
            'height': height
        }))

    def resize_column(self, column, width):
        self._view.add_event(event.Event('ColumnResized', {
            'column': column,
            'width': width
        }))

    def _new_file(self):
        self._view.add_event(event.Event('NewFile'))

    def _open_file(self):
        open_file_name = fd.askopenfilename(filetypes=(('HexSheets', '*.hxs'),
                                                       ('All Files', '*.*')))
        self._view.add_event(event.Event('OpenFile', {'filename': open_file_name}))

    def update_save_option(self, option):
        self._save_option_allowed = option

    def _save_file(self):
        if self._save_option_allowed:
            self._view.add_event(event.Event('SaveFile'))
        else:
            self._save_file_as()

    def _save_file_as(self):
        save_file_name = fd.asksaveasfilename(defaultextension='hxs',
                                              filetypes=(('HexSheets', '*.hxs'),
                                                         ('All Files', '*.*')))
        self._view.add_event(event.Event('SaveFileAs', {'filename': save_file_name}))

    def _help(self):
        webbrowser.open_new(os.getcwd() + '/docs/index.html')
