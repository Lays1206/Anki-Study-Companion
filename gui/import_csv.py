from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog
from pathlib import Path

from data.csv_handler import load_terms
from automation.browser import Browser


class ImportCSV(QWidget):
    csv_imported = pyqtSignal()
    word_skipped = pyqtSignal()
    marked_complete = pyqtSignal()
    words_checked = pyqtSignal()

    def __init__(self, database, anki_connect):
        super().__init__()

        self.database = database
        self.anki = anki_connect
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout()

        self.btn = QPushButton("Upload CSV file")
        self.btn.setObjectName("import")
        self.btn.setFixedSize(120, 30)
        self.btn.setStyleSheet("""
                               QPushButton#import {
                                font-size: 14px; 
                                font-weight: normal; 
                                border: none;
                                border-radius: 3px;
                                background-color: #ebedeb;
                                color: #222;
                        
                               }

                               QPushButton#import:disabled {
                                background-color: rgba(225, 227, 225, 100);
                                color: rgba(34, 34, 34, 80);
                               }

                          """)
        
        self.btn.clicked.connect(self.open_file)
        
        self.load_status = QLabel()
        self.file_label = QLabel()

        browser_btn_layout = QHBoxLayout()

        self.init_browser = QPushButton("Start word queue")
        self.init_browser.clicked.connect(self.open_browser)

        browser_btn_layout.addWidget(self.init_browser, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.close_browser = QPushButton("Close browser")
        self.close_browser.setDisabled(True)
        self.close_browser.clicked.connect(self.exit_browser)

        browser_btn_layout.addWidget(self.close_browser, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.current_term = QLabel("")
        self.current_term.setStyleSheet("font-size: 18px; font-weight: bold")

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        self.skip_btn = QPushButton("Skip this word")
        #self.skip_btn.setFixedSize(120, 30)
        self.skip_btn.setStyleSheet("font-size: 14px")

        self.skip_btn.clicked.connect(self.skip_word)
        self.skip_btn.setDisabled(True)

        self.complete_btn = QPushButton("Mark complete")
        #self.complete_btn.setFixedSize(120, 30)
        self.complete_btn.setStyleSheet("font-size: 14px")
        
        self.complete_btn.clicked.connect(self.mark_complete)
        self.complete_btn.setDisabled(True)

        btn_layout.addWidget(self.skip_btn)
        btn_layout.addWidget(self.complete_btn)
        
        layout.addWidget(self.btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.load_status, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.file_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(browser_btn_layout)

        layout.addStretch()

        layout.addWidget(self.current_term, alignment=Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch()
        
        layout.addLayout(btn_layout)

        layout.setContentsMargins(20, 20, 20, 50)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(layout)
    

    # Handles CSV file uploads and emits a signal to the queue
    def open_file(self):
        self.load_status.setText("Accessing files...")
        file_path, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*csv)")

        if file_path:
            terms = load_terms(file_path)
            for term in terms:
                self.database.add_word(term) 

            self.load_status.setText("Complete!")

            self.file_label.setText(f"You have successfully uploaded '{Path(file_path).name}'")
            self.csv_imported.emit()

    
    # Handles browser initialization and removes unneeded words from database
    def open_browser(self):
        existing_terms = self.anki.get_deck_words()

        self.current_index = 0

        new_terms = []
        incomplete_terms = self.database.get_incomplete_words()
        for term in incomplete_terms:
            if term[0] not in existing_terms:
                new_terms.append(term[0]) 

            else:
                self.database.remove_word(term[0])
            
            self.words_checked.emit()
        
        self.new_terms = new_terms 

        if new_terms:
            self.browser = Browser()
            self.browser.start()

            self.process_term()
            
            self.close_browser.setDisabled(False)

        else:
            self.current_term.setText("No new words to add.")
    
    
    # Wrapper method for closing browser instance
    def exit_browser(self):
        self.current_term.setText("")
        self.close_browser.setDisabled(True)

        self.browser.close()
        

    # Handles word search and updating word status upon processing
    def process_term(self):
        if self.current_index >= len(self.new_terms):
            self.skip_btn.setDisabled(True)
            self.complete_btn.setDisabled(True)

            self.current_term.setText("All done!")
    
            return

        term = self.new_terms[self.current_index]

        self.database.update_status(term, 'processing')

        self.current_term.setText(f"Current term: {term}")
        self.browser.word_search(term)

        self.skip_btn.setDisabled(False)
        self.complete_btn.setDisabled(False)


    # Skips a specific word and increments the positional index
    def skip_word(self):
        self.skip_btn.setDisabled(True)
        term = self.new_terms[self.current_index]

        self.current_index += 1

        self.database.update_status(term, 'skipped')
        self.word_skipped.emit()

        self.process_term()

    
    # Marks a specific word for completeness and increments the positional index
    def mark_complete(self):
        self.complete_btn.setDisabled(True)
        term = self.new_terms[self.current_index]

        self.current_index += 1

        self.database.update_status(term, 'completed')
        self.marked_complete.emit()

        self.process_term()


