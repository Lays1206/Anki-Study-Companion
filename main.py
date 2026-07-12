from data.csv_handler import load_terms
from automation.browser import Browser
from anki.anki_connect import AnkiConnect
from data.database import Database
from gui.main_window import MainWindow

from PyQt6.QtWidgets import QApplication


def main():
    # terms = load_terms("vocab.csv")

    # anki = AnkiConnect()
    # existing_terms = anki.get_deck_words()

    # new_terms = [ term for term in terms 
    #                if term not in existing_terms ]
    
    # print(f"Words not in deck: {len(new_terms)}")
    
    # browser = Browser() 
    # browser.start()

    # for i, term in enumerate(new_terms):
    #    print(f"Processing {i+1}/{len(new_terms)}: {term}")
    #    browser.word_search(term)
    #    input("Press Enter to continue...")
    
    # browser.close()

    db = Database("data/sample.db")

    app = QApplication([])

    window = MainWindow(db)
    window.show()

    app.exec()

    db.close()



if __name__ == "__main__":
    main()




