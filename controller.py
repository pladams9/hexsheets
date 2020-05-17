import view
import tkinter as tk


class Controller:
    def __init__(self):
        self.model = None
        self.tk_root = tk.Tk()
        self.view = view.View(self.tk_root)

        # Event Bindings
        def cell_select(event):
            self.view.set_value('status_bar', str(event.widget.current_cell))
            self.view.set_value('cell_values', {event.widget.current_cell: 'new_value'})

        self.tk_root.bind('<<HexCells_Selected>>', cell_select)

    def start(self):
        self.tk_root.mainloop()