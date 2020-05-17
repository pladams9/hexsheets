import tkinter as tk
import gui.widgets


class MainWindow:
    def __init__(self, parent_view, tk_root):
        self.parent_view = parent_view
        self.tk_root = tk_root

        tk_root.title('Hexagonal Spreadsheet')
        tk_root.geometry('800x600')

        menu_bar = tk.Menu(tk_root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New...")
        file_menu.add_command(label="Open...")
        file_menu.add_command(label="Save...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=tk_root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        tk_root.configure(menu=menu_bar)

        tk_root.rowconfigure(0, weight=1)
        tk_root.columnconfigure(0, weight=1)
        mainframe = tk.Frame(tk_root)
        mainframe.grid(sticky='nsew')
        mainframe.rowconfigure(1, weight=1)
        mainframe.columnconfigure(0, weight=1)

        top_bar = tk.Frame(mainframe)
        top_bar.grid(column=0, row=0, sticky='nsew')
        top_bar.columnconfigure(0, weight=1)

        tool_bar = tk.Frame(top_bar)
        tk.Button(tool_bar, text='Test').pack(side=tk.LEFT)
        tool_bar.grid(column=0, row=0, sticky='we')

        formula_bar = tk.Frame(top_bar)
        formula_bar.grid(column=0, row=1, sticky='we')
        tk.Label(formula_bar, text='Formula:').pack(side=tk.LEFT)

        self.formula_box = tk.Entry(
            formula_bar,
            validate='key',
            vcmd=self._enter_formula
        )
        self.formula_box.pack(fill=tk.X)
        self.parent_view.add_observer('formula_box', self.update_formula_box)

        self.spreadsheet = gui.widgets.HexCells(mainframe, hex_rows=20, hex_columns=20)
        self.spreadsheet.grid(column=0, row=1, sticky='nsew')
        self.parent_view.add_observer('cell_values', self.spreadsheet.set_cell_values)

        self.status_bar = tk.Label(mainframe, relief=tk.GROOVE, anchor=tk.W)
        self.status_bar.grid(column=0, row=2, sticky=(tk.W, tk.E))
        self.parent_view.add_observer('status_bar', self.update_status_bar)

    def update_status_bar(self, text):
        self.status_bar.config(text=text)

    def _enter_formula(self):
        self.formula_box.event_generate('<<FormulaChanged>>', when='tail')
        return True

    def update_formula_box(self, text):
        self.formula_box.delete(0, tk.END)
        self.formula_box.insert(0, text)
