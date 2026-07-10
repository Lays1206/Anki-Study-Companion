import requests


class AnkiConnect:

    def __init__(self):
        self.url = 'http://localhost:8765'


    def get_deck_words(self):

        payload= {
            "action": "findNotes",
            "version": 5,
            "params": {
            "query": "deck:current"
            }
        }

        response = requests.post(self.url, json=payload)
        note_ids = response.json()["result"]

        payload = {
            "action": "notesInfo",
            "version": 5,
            "params": {
            "notes": note_ids
            }
        }

        response = requests.post(self.url, json=payload)
        notes = response.json()["result"]

        words = []

        for note in notes:
            word = note["fields"]["front"]["value"]
            words.append(word)
        
        return words

