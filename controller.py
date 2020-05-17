import view
import tkinter as tk
import model


class Controller:
    def __init__(self):
        self.model = model.Model()
        self.tk_root = tk.Tk()
        self.view = view.View(self.tk_root)

        # Event Bindings
        def cell_select(event):
            xy = event.widget.current_cell
            self.model.select_cell(xy[0], xy[1])
            self.view.set_value('formula_box', self.model.get__selected_cell_formula())

            self.view.set_value('status_bar', str(event.widget.current_cell))

        self.tk_root.bind('<<HexCells_Selected>>', cell_select)

        def formula_changed(event):
            self.model.set_selected_cell_formula(event.widget.get())
            self.view.set_value('cell_values', self.model.get_cell_values())

        self.tk_root.bind('<<FormulaChanged>>', formula_changed)

    def start(self):
        self.tk_root.mainloop()