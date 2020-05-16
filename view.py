import gui.windows


class View:
    def __init__(self, root):
        self.root = root

        self.main_window = gui.windows.MainWindow(root)

    def start(self):
        self.root.mainloop()
