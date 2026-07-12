from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class Statistics(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        label = QLabel("This is the statistics page for deck/vocabulary data.")
        layout = QVBoxLayout()

        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)
        

