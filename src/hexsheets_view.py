from tk_mvc import View
import gui.windows


class HexSheetsView(View):
    def __init__(self, tk_root):
        super().__init__(tk_root)

        # Windows
        self.main_window = gui.windows.MainWindow(self, tk_root)
