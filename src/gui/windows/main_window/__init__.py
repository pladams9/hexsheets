from tk_mvc import BaseWindow
import tkinter as tk
from tk_mvc import Event
from gui.windows.main_window.top_area import TopArea
from gui.windows.main_window.spreadsheet_area import SpreadsheetArea
from gui.windows.main_window.menu import MainWindowMenu


class MainWindow(BaseWindow):
    def __init__(self, view, window):
        super().__init__(view, window)

        self._view.add_observer('title', self.update_title)
        self._window.protocol("WM_DELETE_WINDOW", self._window.quit)

        self._window.geometry('800x600')
        self._window.rowconfigure(0, weight=1)
        self._window.columnconfigure(0, weight=1)
        self.grid(sticky='nsew')
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Menu Bar
        self.menu = MainWindowMenu(self._view, self._window)

        # Top Area
        self.top_area = TopArea(self._view, self)
        self.top_area.grid(column=0, row=0, sticky='nsew')
        self._view.add_observer('formula_box', self.update_formula_box)

        # Spreadsheet Area
        self.spreadsheet_area = SpreadsheetArea(self._view, self)
        self.spreadsheet_area.grid(column=0, row=1, sticky='nsew')

        # Formula Box Commands
        self._formula_box = self.top_area.formula_box
        vcmd = (self.register(self._enter_formula), '%P')
        self._formula_box.config(vcmd=vcmd)
        self._formula_box.bind("<FocusIn>", lambda e: e.widget.config(validate='key'))
        self._formula_box.bind("<FocusOut>", lambda e: e.widget.config(validate='none'))

        # Status Bar
        self.status_bar = tk.Label(self, relief=tk.GROOVE, anchor=tk.W)
        self.status_bar.grid(column=0, row=2, sticky=(tk.W, tk.E))
        self._view.add_observer('status_bar', self.update_status_bar)

    def update_status_bar(self, text):
        self.status_bar.config(text=text)

    def update_title(self, text):
        self._window.title('HexSheets - ' + text)

    def _enter_formula(self, new_text):
        self._view.add_event(Event('FormulaChanged', {'formula': new_text}))
        return True

    def update_formula_box(self, text):
        validation = self._formula_box.cget('validate')
        self._formula_box.config(validate='none')
        self._formula_box.delete(0, tk.END)
        self._formula_box.insert(0, text)
        self._formula_box.config(validate=validation)
