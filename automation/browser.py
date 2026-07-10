from selenium import webdriver


class Browser:

    def __init__(self):
        self.driver = None


    def start(self):
        self.driver = webdriver.Chrome()


    def word_search(self, word):
        url = f"https://www.kanshudo.com/searcht?q={word}"
        self.driver.get(url)


    def close(self):
        self.driver.quit()