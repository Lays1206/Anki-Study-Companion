from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.database = database
