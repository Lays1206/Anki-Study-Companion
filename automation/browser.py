from selenium import webdriver
from selenium.webdriver.firefox.options import Options


class Browser:

    def __init__(self):
        self.driver = None


    def start(self):
        options = Options()

        # Add path to firefox profile with yomitan extension installed
        profile_path = r"C:\Users\layla\AppData\Roaming\Mozilla\Firefox\Profiles\xs8kkyn2.default-release"
        options.add_argument(f"-profile={profile_path}")

        self.driver = webdriver.Firefox(options=options)


    def word_search(self, word):
        # Other sentence search sites will work, this one is just a preference
        url = f"https://sentencesearch.neocities.org/#{word}"
        self.driver.get(url)


    def close(self):
        self.driver.quit()