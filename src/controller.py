import view
import tkinter as tk
import model


class Controller:
    def __init__(self):
        self.model = model.Model()
        self.tk_root = tk.Tk()
        self.view = view.View(self.tk_root)

        self._event_handlers = {
            'FormulaChanged': self.formula_changed,
            'CellSelected': self.cell_selected,
            'NewFile': self.new_file,
            'OpenFile': self.open_file,
            'SaveFile': self.save_file
        }

    def start(self):
        self.tk_root.after(100, self.handle_events)
        self.tk_root.mainloop()

    def handle_events(self):
        for e in self.view.get_events():
            if e.type in self._event_handlers:
                self._event_handlers[e.type](e)

        self.tk_root.after(100, self.handle_events)

    def formula_changed(self, e):
        self.model.set_selected_cell_formula(e.data['formula'])
        self.model.editing_cell = True
        self.view.set_value('cell_values', self.model.get_cell_values())

    def cell_selected(self, e):
        xy = e.data['address']
        self.model.select_cell(xy[0], xy[1])

        if self.model.editing_cell:
            self.view.set_value('cell_values', self.model.get_cell_values())
            self.model.editing_cell = False

        self.view.set_value('formula_box', self.model.get_selected_cell_formula())
        self.view.set_value('status_bar', str(xy))

    def new_file(self, e):
        self.model.new_file()
        self.view.set_value('cell_values', self.model.get_cell_values())

    def open_file(self, e):
        self.model.open_file(e.data['filename'])
        self.view.set_value('cell_values', self.model.get_cell_values())

    def save_file(self, e):
        self.model.save_file(e.data['filename'])
