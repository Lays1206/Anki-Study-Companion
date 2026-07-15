from anki.anki_connect import AnkiConnect
from data.database import Database
from gui.main_window import MainWindow

from PyQt6.QtWidgets import QApplication
import os
import sys


def main():

    if len(sys.argv) < 2:
        print("Error: Please provide a file path.")
        sys.exit()
    
    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: The path '{file_path}' does not exist.")
        sys.exit()

    print(f"Successfully located file '{file_path}'! Setting up database...")
    
    db = Database(file_path)

    anki = AnkiConnect()

    app = QApplication([])

    window = MainWindow(db, anki)
    window.show()

    app.exec()

    db.close()


if __name__ == "__main__":
    main()




