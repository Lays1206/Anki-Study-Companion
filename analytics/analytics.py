import datetime as dt


class Analytics:
    def __init__(self, database, anki_connect, deck_name):
        self.database = database
        self.anki = anki_connect
        self.deck_name = deck_name
    
    def total_reviews_today(self):
        return self.anki.word_reviews_today()
        # return total reviews today (entire collection)

    def reviews_this_week(self):
        reviews = self.anki.card_reviews(self.deck_name, start_id=0)
        past_week = dt.datetime.now() - dt.timedelta(days=7)
        past_week_ms = int(past_week.timestamp() * 1000)

        past_week_reviews = [r for r in reviews if r[0] >= past_week_ms]
        return len(past_week_reviews)
        # compute total reviews for the past week

    def reviews_this_month(self):
        reviews = self.anki.card_reviews(self.deck_name, start_id=0)
        past_month = dt.datetime.now() - dt.timedelta(days=30)
        past_month_ms = int(past_month.timestamp() * 1000)

        past_month_reviews = [r for r in reviews if r[0] >= past_month_ms]
        return len(past_month_reviews)
        # compute total reviews for the past month
    
    def card_counts(self):
        deck_id = str(self.anki.deck_names_ids()[self.deck_name])
        deck_stats = self.anki.deck_stats([self.deck_name])[deck_id]

        return deck_stats
        # return dict of all card types (new/in-learning/due-for-review/total)

    def average_review_time(self):
        reviews = self.anki.card_reviews(self.deck_name, start_id=0)

        total_duration = 0
        for r in reviews:
            total_duration += r[7]
        
        try: 
            average_duration = total_duration / len(reviews)
            return round(average_duration, 2)
        except ZeroDivisionError:
            return 0
        # compute average of review duration for entire deck
    
    def group_by_month(self, reviews):
        today = dt.date.today()
    
        total_reviews = {
            1: [0]*2, 2: [0]*2, 3: [0]*2,
            4: [0]*2, 5: [0]*2, 6: [0]*2, 
            7: [0]*2, 8: [0]*2, 9: [0]*2, 
            10: [0]*2, 11: [0]*2, 12: [0]*2
        }

        reviews_this_year = [ r for r in reviews if dt.date.fromtimestamp(r[0] / 1000) 
                             if dt.date.fromtimestamp(r[0] / 1000).year == today.year]
        for r in reviews_this_year:
            r[0] = dt.date.fromtimestamp(r[0] / 1000)
            current_month = r[0].month
            total_reviews[current_month][0] += 1
            if r[3] == 1:
                total_reviews[current_month][1] += 1
        return total_reviews
    
    def accuracy_rate(self):
        reviews = self.anki.card_reviews(self.deck_name, start_id=0)
        review_dates = self.group_by_month(reviews)

        accuracy_rate = {
            1: 0, 2: 0, 3: 0,
            4: 0, 5: 0, 6: 0,
            7: 0, 8: 0, 9: 0,
            10: 0, 11: 0, 12: 0
        }

        for month, count in review_dates.items():
            try:
                accuracy_rate[month] = round(1 - (count[1] / count[0]), 2) * 100
            except ZeroDivisionError:
                continue
        
        return accuracy_rate
        # compute accuracy rate
    
    def calculate_streak(self):
        reviews = self.anki.card_reviews(self.deck_name, start_id=0)

        review_dates = { dt.date.fromtimestamp(r[0] / 1000) for r in reviews }

        today = dt.date.today()
        streak = 0

        current_day = today if today in review_dates else today - dt.timedelta(days=1)
        while current_day in review_dates:
            streak += 1
            current_day -= dt.timedelta(days=1)
        
        return streak
        # return streak of consecutive days where at least 1 word reviewed

    def completion_rate(self):
        complete_words = self.database.get_complete_words()
        all_words = self.database.get_all_words()

        try: 
            complete_rate = len(complete_words) / len(all_words)
            return round(complete_rate, 2)
        except ZeroDivisionError:
            return 0
        # calculate % completed vs skipped/pending/processing
        
