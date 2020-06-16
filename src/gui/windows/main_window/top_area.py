import tkinter as tk
import tkinter.font as tkf
from tk_mvc import WindowPart, Event


class TopArea(WindowPart):
    def _build(self):
        self.columnconfigure(0, weight=1)

        # Tool Bar
        tool_bar = tk.Frame(self)
        tool_bar.grid(column=0, row=0, sticky='we')
        buttons = [
            tk.Button(tool_bar, text='B', font=tkf.Font(weight='bold'), state=tk.DISABLED,
                      command=lambda: self._view.add_event(Event('ToggleBold'))),
            tk.Button(tool_bar, text='I', font=tkf.Font(slant='italic'), state=tk.DISABLED,
                      command=lambda: self._view.add_event(Event('ToggleItalic'))),
            tk.Button(tool_bar, text='U', font=tkf.Font(underline=1), state=tk.DISABLED,
                      command=lambda: self._view.add_event(Event('ToggleUnderline')))
        ]
        for button in buttons:
            button.pack(side=tk.LEFT, fill=tk.Y)

        # Formula Bar
        formula_bar = tk.Frame(self)
        formula_bar.grid(column=0, row=1, sticky='we')
        tk.Label(formula_bar, text='Formula:').pack(side=tk.LEFT)

        self.formula_box = tk.Entry(formula_bar)
        self.formula_box.pack(fill=tk.X)
