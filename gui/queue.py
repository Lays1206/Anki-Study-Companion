from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

    
# Creates a single widget for individual rows in the database
class QueueItem(QWidget):
    def __init__(self, row, index):
        super().__init__()
        self.id, self.reading, self.status, self.timestamp = row

        layout = QHBoxLayout()

        #index_label = QLabel(f"{index + 1}) ")
        reading_label = QLabel(self.reading)
        reading_label.setFixedWidth(215)
        self.status_label = QLabel(self.status)
        timestamp_label = QLabel(self.timestamp)

        self.setStyleSheet('QLabel{font-size: 14px}')

        #layout.addWidget(index_label)
        layout.addWidget(reading_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(timestamp_label, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.color_status()

        self.setLayout(layout)
    
    def color_status(self):
        if self.status == 'pending':
            self.status_label.setStyleSheet("color: #fcfa56")
        
        elif self.status == 'processing':
            self.status_label.setStyleSheet("color: #fcc256")
        
        elif self.status == 'completed':
            self.status_label.setStyleSheet("color: #1bab61; font-weight: bold")
        
        elif self.status == 'skipped':
            self.status_label.setStyleSheet("color: #e64c35")


# Queue containing all queue widgets
class Queue(QWidget):
    PAGE_SIZE = 10

    def __init__(self, database, anki_connect):
        super().__init__()

        self.database = database
        self.anki = anki_connect
        self.current_page = 0
        self.rows = []
        self.item_widgets = []
    
        self.initUI()
    

    def initUI(self):
        self.layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh queue")
        self.refresh_btn.clicked.connect(self.refresh_queue)

        label = QLabel("")
   
        font = label.font()
        font.setUnderline(True)

        reading = QLabel("Reading")
        reading.setFont(font)
        status = QLabel("Status")
        status.setFont(font)
        timestamp = QLabel("Date added")
        timestamp.setFont(font)

        header_layout = QHBoxLayout()
        #header_layout.addWidget(label)
        header_layout.addWidget(reading, alignment=Qt.AlignmentFlag.AlignHCenter)
        header_layout.addWidget(status, alignment=Qt.AlignmentFlag.AlignHCenter)
        header_layout.addWidget(timestamp, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.layout.addWidget(self.refresh_btn, alignment=Qt.AlignmentFlag.AlignHCenter)
        
        self.layout.addLayout(header_layout)

        self.items_layout = QVBoxLayout()
        self.layout.addLayout(self.items_layout)

        self.layout.addStretch()
        
        self.back_btn = QPushButton("Back")
        self.back_btn.clicked.connect(self.go_back)

        self.page_num = QLabel("")

        self.next_btn = QPushButton("Next")
        self.next_btn.clicked.connect(self.go_next)

        self.btn_layout.addWidget(self.back_btn)
        self.btn_layout.addWidget(self.page_num, alignment=Qt.AlignmentFlag.AlignHCenter)
        self.btn_layout.addWidget(self.next_btn)

        self.layout.addLayout(self.btn_layout)

        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setContentsMargins(10, 0, 0, 0)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.load_rows()
    

    def load_rows(self):
        self.rows = self.database.get_all_words()
        self.render_page()

    
    # Handles re-rendering the page for each page update
    def render_page(self):
        for widget in self.item_widgets:
            self.items_layout.removeWidget(widget)
            widget.deleteLater()
        self.item_widgets.clear()

        start = self.current_page * self.PAGE_SIZE
        end = start + self.PAGE_SIZE
        page_rows = self.rows[start:end]

        for i, row in enumerate(page_rows):
            item = QueueItem(row, i + start) # Will later implement item numbering
            self.items_layout.addWidget(item)
            self.item_widgets.append(item)
        
        self.page_num.setText(f"{self.current_page + 1}")
        self.back_btn.setDisabled(self.current_page == 0)
        self.next_btn.setDisabled(end >= len(self.rows))


    def go_back(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.render_page()

    
    def go_next(self):
        if (self.current_page + 1) * self.PAGE_SIZE < len(self.rows):
            self.current_page += 1
            self.render_page()

    
    def refresh_queue(self):
        self.refresh_btn.setText("Refreshing...")
        self.refresh_btn.setDisabled(True)

        QApplication.processEvents()

        self.check_queue()

        self.refresh_btn.setText("Refresh queue")
        self.refresh_btn.setDisabled(False)


    def check_queue(self):
        existing_terms = self.anki.get_deck_words()

        incomplete_terms = self.database.get_incomplete_words()
        for term in incomplete_terms:
            if term[0] in existing_terms:
                self.database.remove_word(term[0])
        
        self.load_rows()
        
    

        

