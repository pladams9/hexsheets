import tkinter as tk
import gui.widgets


class MainWindow(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        master.title('Hexagonal Spreadsheet')
        master.geometry('800x600')

        menu_bar = tk.Menu(master)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New...")
        file_menu.add_command(label="Open...")
        file_menu.add_command(label="Save...")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        master.configure(menu=menu_bar)

        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        mainframe = tk.Frame(master)
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
        tk.Entry(formula_bar).pack(fill=tk.X)

        spreadsheet = gui.widgets.HexCells(mainframe, hex_rows=5, hex_columns=5)
        spreadsheet.grid(column=0, row=1, sticky='nsew')

        self.status_bar = tk.Label(mainframe, relief=tk.GROOVE, anchor=tk.W)
        self.status_bar.grid(column=0, row=2, sticky=(tk.W, tk.E))

    def update_status_bar(self, text):
        self.status_bar.config(text=text)
