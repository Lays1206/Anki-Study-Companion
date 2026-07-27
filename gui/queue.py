from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QScrollArea, QDialog, QDialogButtonBox, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton

class ResetDialog(QDialog):
    def __init__(self):
        super().__init__()

        options = (
            QDialogButtonBox.StandardButton.Yes | QDialogButtonBox.StandardButton.No
        )

        self.setWindowTitle(" ")
        self.setWindowIcon(QIcon("images\warning.png"))

        self.button_box = QDialogButtonBox(options)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout()
        message = QLabel("This action cannot be reset. Are you sure?")
        layout.addWidget(message)
        layout.addWidget(self.button_box)
        self.setLayout(layout)


# Creates a single widget for individual rows in the database
class QueueItem(QWidget):
    word_deleted = pyqtSignal()

    def __init__(self, row, database):
        super().__init__()

        self.database = database
        self.id, self.reading, self.status, self.timestamp = row

        layout = QHBoxLayout()

        reading_label = QLabel(self.reading)
        reading_label.setFixedWidth(130)
        reading_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.status_label = QLabel(self.status)
        timestamp_label = QLabel(self.timestamp)

        self.delete_btn = QPushButton("Delete?")
        self.delete_btn.clicked.connect(self.delete_word)

        self.setStyleSheet("""QLabel {font-size: 14px}""")

        layout.addWidget(reading_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(timestamp_label, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.delete_btn, alignment=Qt.AlignmentFlag.AlignRight)

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

    
    def delete_word(self):
        self.database.remove_word(self.reading)
        self.word_deleted.emit()


# Queue containing all queue widgets
class Queue(QWidget):
    PAGE_SIZE = 10

    def __init__(self, database, anki_connect, deck_name):
        super().__init__()

        self.database = database
        self.anki = anki_connect
        self.deck_name = deck_name
        self.current_page = 0
        self.rows = []
        self.item_widgets = []
    
        self.initUI()
    

    def initUI(self):
        outer_layout = QVBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        container.setObjectName("container")

        self.layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        container.setLayout(self.layout)
        container.setStyleSheet("QWidget#container {background-color: #2b2b2b; border: none}")

        scroll.setWidget(container)
        outer_layout.addWidget(scroll)

        top_btn_layout = QHBoxLayout()

        self.refresh_btn = QPushButton("Refresh queue")
        self.refresh_btn.clicked.connect(self.refresh_queue)

        self.reset_btn = QPushButton("Mark all as in progress")
        self.reset_btn.clicked.connect(self.reset_queue)

        top_btn_layout.addWidget(self.refresh_btn)
        top_btn_layout.addWidget(self.reset_btn)

        top_btn_layout.setContentsMargins(80, 0, 80, 0)
        top_btn_layout.setSpacing(30)

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
        header_layout.addWidget(reading, alignment=Qt.AlignmentFlag.AlignHCenter)
        header_layout.addWidget(status, alignment=Qt.AlignmentFlag.AlignHCenter)
        header_layout.addWidget(timestamp, alignment=Qt.AlignmentFlag.AlignHCenter)
        header_layout.addWidget(label)

        self.layout.addLayout(top_btn_layout)
        
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
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)
        self.setLayout(outer_layout)

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

        for row in page_rows:
            item = QueueItem(row, self.database)
            item.word_deleted.connect(self.load_rows)
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

        self.rows = self.database.get_all_words()

        self.refresh_btn.setText("Refresh queue")
        self.refresh_btn.setDisabled(False)


    def reset_queue(self):
        dlg = ResetDialog()
        if dlg.exec():
            self.reset_btn.setDisabled(True)

            QApplication.processEvents()

            terms = self.database.get_all_words()

            for term in terms:
                self.database.update_status(term[1], "pending")

            self.load_rows()

            self.reset_btn.setDisabled(False)


    def check_queue(self):
        existing_terms = self.anki.get_deck_words(self.deck_name)

        incomplete_terms = self.database.get_incomplete_words()
        for term in incomplete_terms:
            if term[0] in existing_terms:
                self.database.remove_word(term[0])

    

        

