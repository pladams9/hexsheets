from tk_mvc import View
import gui.windows


class HexSheetsView(View):
    def __init__(self):
        super().__init__()

        # Windows
        self.main_window = gui.windows.MainWindow(self, self._tk_root)
