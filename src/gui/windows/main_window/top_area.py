import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkf
import tkinter.colorchooser as tkc
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

        self._font_size = tk.StringVar()
        self._font_size.set('14')
        self.font_trace = self._font_size.trace('w', self._change_font_size)
        font_size_options = ['8', '9', '10', '11', '12', '14', '16', '18', '20', '24', '32', '48', '72']
        font_size_dropdown = ttk.Combobox(tool_bar, textvariable=self._font_size, values=font_size_options,
                                          justify=tk.RIGHT, width=3)
        font_size_dropdown.pack(side=tk.LEFT)
        self._view.add_observer('current_cell_font_size', self.update_current_cell_font_size)

        self._font_color_button = tk.Frame(tool_bar, bg='#EEE', bd=2, relief=tk.SUNKEN, width=32, height=32)
        self._font_color_button.pack_propagate(0)
        self._font_A = tk.Label(self._font_color_button, text='A', bg='#EEE')
        self._font_A.pack(expand=True, fill=tk.BOTH)
        self._font_color_button.bind('<ButtonRelease-1>', self._click_font_color)
        self._font_A.bind('<ButtonRelease-1>', self._click_font_color)
        self._font_color_button.pack(side=tk.LEFT)
        self._view.add_observer('current_cell_font_color', self.update_current_cell_font_color)

        self._cell_color_button = tk.Frame(tool_bar, bg='#EEE',  bd=2, relief=tk.SUNKEN, width=32, height=32)
        self._cell_color_button.bind('<ButtonRelease-1>', self._click_cell_color)
        self._cell_color_button.pack(side=tk.LEFT)
        self._view.add_observer('current_cell_color', self.update_current_cell_color)

        # Formula Bar
        formula_bar = tk.Frame(self)
        formula_bar.grid(column=0, row=1, sticky='we')
        tk.Label(formula_bar, text='Formula:').pack(side=tk.LEFT)

        self.formula_box = tk.Entry(formula_bar)
        self.formula_box.pack(fill=tk.X)
        self.formula_box.bind('<Return>', lambda e: self._view.add_event(Event('ExitEditMode', data={'complete': True})))
        self.formula_box.bind('<Escape>', lambda e: self._view.add_event(Event('ExitEditMode', data={'complete': False})))

        self._view.add_observer('formula_box', self.update_formula_box)

        vcmd = (self.register(self._enter_formula), '%P')
        self.formula_box.config(vcmd=vcmd)
        self.formula_box.bind("<FocusIn>", lambda e: e.widget.config(validate='key'))
        self.formula_box.bind("<FocusOut>", lambda e: e.widget.config(validate='none'))
        self._view.add_observer('editing_mode', self._change_edit_mode)

    def _click_cell_color(self, e):
        new_color = tkc.askcolor(title='Set Cell Color', color=e.widget.cget('color'))
        self._view.add_event(Event(
            'SetCellColor',
            {'color': new_color[1]}
        ))

    def update_current_cell_color(self, color):
        self._cell_color_button.config(bg=color)

    def _click_font_color(self, e):
        new_color = tkc.askcolor(title='Set Cell Color', color=self._font_color_button.cget('color'))
        self._view.add_event(Event(
            'SetFontColor',
            {'color': new_color[1]}
        ))

    def update_current_cell_font_color(self, color):
        self._font_A.config(fg=color)

    def _change_font_size(self, *args, **kwargs):
        self._view.add_event(Event('SetFontSize', data={
            'font_size': int(self._font_size.get())
        }))

    def update_current_cell_font_size(self, size: int):
        self._font_size.trace_vdelete('w', self.font_trace)
        self._font_size.set(str(size))
        self.font_trace = self._font_size.trace('w', self._change_font_size)

    def _enter_formula(self, new_text):
        self._view.add_event(Event('FormulaChanged', {'formula': new_text}))
        return True

    def update_formula_box(self, text):
        validation = self.formula_box.cget('validate')
        self.formula_box.config(validate='none')
        self.formula_box.delete(0, tk.END)
        self.formula_box.insert(0, text)
        self.formula_box.config(validate=validation)

    def _change_edit_mode(self, edit_mode):
        if edit_mode:
            self.formula_box.focus_set()
