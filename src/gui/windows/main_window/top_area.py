import tkinter as tk
import tkinter.font as tkf
from tk_mvc import WindowPart


class TopArea(WindowPart):
    def _build(self):
        self.columnconfigure(0, weight=1)

        # Tool Bar
        tool_bar = tk.Frame(self)
        tk.Button(tool_bar, text='B', font=tkf.Font(weight='bold')).pack(side=tk.LEFT, fill=tk.Y)
        tk.Button(tool_bar, text='I', font=tkf.Font(slant='italic')).pack(side=tk.LEFT, fill=tk.Y)
        tk.Button(tool_bar, text='U', font=tkf.Font(underline=1)).pack(side=tk.LEFT, fill=tk.Y)
        tool_bar.grid(column=0, row=0, sticky='we')

        # Formula Bar
        formula_bar = tk.Frame(self)
        formula_bar.grid(column=0, row=1, sticky='we')
        tk.Label(formula_bar, text='Formula:').pack(side=tk.LEFT)

        self.formula_box = tk.Entry(formula_bar)
        self.formula_box.pack(fill=tk.X)
