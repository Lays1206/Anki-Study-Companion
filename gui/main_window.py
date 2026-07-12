from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QStackedWidget,
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton, 
)
from .import_csv import ImportCSV
from .queue import Queue
from .statistics import Statistics
 

class MainWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()

        self.database = database

        self.center()

        self.initUI()

    def initUI(self):
        self.setFixedSize(650, 550)
    
        self.setWindowTitle("Anki Study Companion")
        self.setWindowIcon(QIcon("images\star.png"))

        page_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        self.pages = QStackedWidget()

        btn = QPushButton("Import CSV")
        btn.setObjectName("button1")
        button_layout.addWidget(btn)
        btn.clicked.connect(self.activate_tab_1)
        self.pages.addWidget(ImportCSV(self.database))

        btn = QPushButton("Queue")
        btn.setObjectName("button2")
        button_layout.addWidget(btn)
        btn.clicked.connect(self.activate_tab_2)
        self.pages.addWidget(Queue(self.database))

        btn = QPushButton("Statistics")
        btn.setObjectName("button3")
        button_layout.addWidget(btn)
        btn.clicked.connect(self.activate_tab_3)
        self.pages.addWidget(Statistics())

        button_layout.setSpacing(0)
        button_layout.setContentsMargins(50, 0, 50, 0)

        page_layout.addLayout(button_layout)
        page_layout.addWidget(self.pages)

        page_layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setObjectName("container")

        widget.setLayout(page_layout)

        widget.setStyleSheet("""
                             #container {
                              background-color: white;
                              color: black;
                            }
            
                             QPushButton#button1,
                             QPushButton#button2,
                             QPushButton#button3 {
                              color: black;
                              font-size: 12px;
                              font-weight: bold;
                              border: 0;
                              background-color: #c7c8c7;
                              padding: 5px;
                            }
                             
                            QPushButton#button1 {
                              border-bottom-left-radius: 5px;
                            }
                             
                            QPushButton#button3 {
                              border-bottom-right-radius: 5px;
                            }
                            
                            QPushButton:hover {
                              border: 1px solid gray;
                            }
      
                            QLabel {
                             color: black
                            }                                                
                            """)

        self.setCentralWidget(widget)

    def activate_tab_1(self):
        self.pages.setCurrentIndex(0)
    
    def activate_tab_2(self):
        self.pages.setCurrentIndex(1)

    def activate_tab_3(self):
        self.pages.setCurrentIndex(2)

    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())