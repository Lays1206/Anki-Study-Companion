from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from pathlib import Path

from data.csv_handler import load_terms

class ImportCSV(QWidget):
    def __init__(self, database):
        super().__init__()

        self.database = database
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.btn = QPushButton("Upload CSV file")
        self.btn.setFixedSize(120, 30)
        self.btn.setStyleSheet("""
                               QPushButton {
                                font-size: 14px; 
                                font-weight: normal; 
                                border: none;
                                border-radius: 3px;
                                background-color: #e1e3e1;
                                color: #222;
                        
                               }

                               QPushButton:disabled {
                                background-color: rgba(225, 227, 225, 100);
                                color: rgba(34, 34, 34, 80);
                               }

                               QPushButton:hover {
                                border: 1px solid #c8c9c8;
                               }
                          
                          """)
        self.btn.clicked.connect(self.open_file)
        
        self.load_status = QLabel()
        self.file_label = QLabel()

        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.load_status, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.file_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.setContentsMargins(0, 50, 0, 0)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)
    
    def open_file(self):
        self.load_status.setText("Loading...")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*csv)")

        if file_path:
            terms = load_terms(file_path)
            for term in terms:
                self.database.add_word(term) 

            self.load_status.setText("Complete!")
            self.btn.setEnabled(False)

            self.file_label.setText(f"You have successfully uploaded '{Path(file_path).name}'")


