from tkinter import Menu
import tkinter.filedialog as fd
import webbrowser
import os
from tk_mvc import Event


class MainWindowMenu:
    def __init__(self, view, window):
        self._view = view

        menu_bar = Menu(window)
        window.config(menu=menu_bar)

        # File Menu
        self.file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="New", command=self._new_file)
        self.file_menu.add_command(label="Open...", command=self._open_file)

        self._save_option_allowed = False
        self._view.add_observer('save_option', self.update_save_option)
        self.file_menu.add_command(label="Save", command=self._save_file)
        self.file_menu.add_command(label="Save As...", command=self._save_file_as)

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Exit", command=window.quit)

        # Help Command
        menu_bar.add_command(label='Help', command=self._help)

    def _new_file(self):
        self._view.add_event(Event('NewFile'))

    def _open_file(self):
        open_file_name = fd.askopenfilename(filetypes=(('HexSheets', '*.hxs'),
                                                       ('All Files', '*.*')))
        self._view.add_event(Event('OpenFile', {'filename': open_file_name}))

    def update_save_option(self, option):
        self._save_option_allowed = option

    def _save_file(self):
        if self._save_option_allowed:
            self._view.add_event(Event('SaveFile'))
        else:
            self._save_file_as()

    def _save_file_as(self):
        save_file_name = fd.asksaveasfilename(defaultextension='hxs',
                                              filetypes=(('HexSheets', '*.hxs'),
                                                         ('All Files', '*.*')))
        self._view.add_event(Event('SaveFileAs', {'filename': save_file_name}))

    def _help(self):
        webbrowser.open_new(os.getcwd() + '/docs/index.html')
