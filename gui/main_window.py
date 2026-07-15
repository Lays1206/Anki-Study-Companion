from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QMainWindow, 
    QWidget, 
    QStackedWidget,
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton,
    QSizePolicy
)
from .import_csv import ImportCSV
from .queue import Queue
from .statistics import Statistics
 

class MainWindow(QMainWindow):
    def __init__(self, database, anki_connect):
        super().__init__()

        self.database = database
        self.anki = anki_connect

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
        btn.setFixedHeight(30)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(btn)
        btn.clicked.connect(self.activate_tab_1)

        import_csv_widget = ImportCSV(self.database, self.anki)
        self.pages.addWidget(import_csv_widget)

        btn = QPushButton("Queue")
        btn.setObjectName("button2")
        btn.setFixedHeight(30)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(btn)
        btn.clicked.connect(self.activate_tab_2)

        queue_widget = Queue(self.database)
        self.pages.addWidget(queue_widget)

        import_csv_widget.csv_imported.connect(queue_widget.load_rows)
        import_csv_widget.word_skipped.connect(queue_widget.load_rows)
        import_csv_widget.marked_complete.connect(queue_widget.load_rows)
        import_csv_widget.words_checked.connect(queue_widget.load_rows)

        btn = QPushButton("Statistics")
        btn.setObjectName("button3")
        btn.setFixedHeight(30)
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        button_layout.addWidget(btn)
        btn.clicked.connect(self.activate_tab_3)
        self.pages.addWidget(Statistics())

        button_layout.setSpacing(0)
        button_layout.setContentsMargins(0, 0, 0, 0)

        page_layout.addLayout(button_layout)
        page_layout.addWidget(self.pages)

        page_layout.setContentsMargins(0, 0, 0, 0)

        widget = QWidget()
        widget.setObjectName("container")

        widget.setLayout(page_layout)

        widget.setStyleSheet("""
                             #container {
                              background-color: #2b2b2b;
                              color: #b0b0b0;
                            }
            
                             QPushButton#button1,
                             QPushButton#button2,
                             QPushButton#button3 {
                              color: #e0e0e0;
                              font-size: 12px;
                              font-weight: bold;
                              border: 1px solid #4287f5;
                              border-radius: 0px;
                              background-color: #4287f5;
                              padding: 5px;
                              min-height: 20px;
                              max-height: 20px;
                            }
                             
                            QPushButton#button1 {
                              border-bottom-left-radius: 5px;
                            }
                            
                            QPushButton#button3 {
                              border-bottom-right-radius: 5px;
                            }
                            
                            QPushButton#button1:hover,
                            QPushButton#button2:hover,
                            QPushButton#button3:hover {
                              border: 1px solid #346bc2;
                            }
      
                            QLabel {
                             color: #b0b0b0;
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
    
