from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

class Queue(QWidget):
    def __init__(self, database):
        super().__init__()

        self.database = database
    
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()
        btn_layout = QHBoxLayout()
    
        label = QLabel("This is the Queue tab.")
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignHCenter)

        for i in range(10):
            label = QLabel(f"{i+1}) Placeholder.")
            layout.addWidget(label)
        
        back_btn = QPushButton("Back")
        next_btn = QPushButton("Next")
        btn_layout.addWidget(back_btn)
        btn_layout.addWidget(next_btn)

        btn_layout.setSpacing(100)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

