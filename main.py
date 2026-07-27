from anki.anki_connect import AnkiConnect
from data.database import Database
from gui.main_window import MainWindow

from PyQt6.QtWidgets import QApplication
import os
import sys
import time


def main():

    if len(sys.argv) < 2:
        print("[ERROR] Please provide a file path.")
        sys.exit()
    
    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"[ERROR] The path '{file_path}' does not exist.")
        sys.exit()

    print(f"[SUCCESS] Located file '{file_path}'! Setting up database...")
    
    db = Database(file_path)

    anki = AnkiConnect()

    app = QApplication([])

    time.sleep(5)
    print("[PLEASE WAIT] Loading main window...")

    window = MainWindow(db, anki, "ENTER DECK NAME") # Enter deck name 
    
    window.show()

    app.exec()

    db.close()


if __name__ == "__main__":
    main()




