import requests


class AnkiConnect:

    def __init__(self):
        self.url = 'http://localhost:8765'


    def invoke(self, action, **params):
        payload = {
            "action": action,
            "version": 6,
            "params": params
        }

        response = requests.get(self.url, json=payload).json()

        if response.get("error") is not None:
            raise Exception(response["error"])

        else:
            return response["result"]
        

    def get_deck_words(self, deck_name):
        note_ids = self.invoke("findNotes", query=f"deck:{deck_name}")  
        notes = self.invoke("notesInfo", notes=note_ids)
    
        words = []

        for note in notes:
            word = note["fields"]["front"]["value"]
            words.append(word)
        
        return words


    def deck_names_ids(self):
        return self.invoke("deckNamesAndIds")


    def word_reviews_today(self):
        return self.invoke("getNumCardsReviewedToday")


    def deck_stats(self, deck_names):
        return self.invoke("getDeckStats", decks=deck_names)


    def card_reviews(self, deck_name, start_id):
       return self.invoke("cardReviews", deck=deck_name, startID=start_id)



