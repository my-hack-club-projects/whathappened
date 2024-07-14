from fake_useragent import UserAgent

import colorama
import requests
import bs4

ua = UserAgent()

class ArticleList:
    def __init__(self, site_data, verbose=False):
        self.name = site_data['name']
        self.url = site_data['url']
        self.headline_element_class = site_data.get('headline_element_class', 'headline')
        self.headline_title_class = site_data.get('headline_title_class', 'headline-title')
        self.minimum_length = site_data.get('minimum_length', 0)

        self.verbose = verbose

        self.headlines = []

    def headline_is_valid(self, headline):
        return len(headline.split()) >= self.minimum_length

    def get_soup(self):
        response = requests.get(self.url, headers={'User-Agent': ua.random})
        response.raise_for_status()
        
        return bs4.BeautifulSoup(response.text, 'html.parser')
    
    def get_headlines(self):
        soup = self.get_soup()

        for headline_title in soup.select(f".{self.headline_title_class}"):
            headline_element = headline_title.find_parent(class_=self.headline_element_class)

            if not headline_element: continue
            if not self.headline_is_valid(headline_title.text): continue

            self.headlines.append(headline_title.text)

        return self.headlines
    
    def summarize(self):
        summarizer = Summarizer('\n'.join(self.headlines))
        return summarizer.summarize()
    
    def __str__(self):
        title = f"{len(self.headlines)} headlines from {self.name}"
        headlines = '\n'.join(self.headlines) if self.verbose else ''

        return colorama.Fore.YELLOW + title + colorama.Fore.RESET + '\n' + headlines
    
class Summarizer:
    MAX_WORD_COUNT = 599
    API_URL = "https://quillbot.com/api/summarizer/summarize-para/abs"
    RATIO = 0.2

    def __init__(self, text):
        self.text = [text[i:i + self.MAX_WORD_COUNT] for i in range(0, len(text), self.MAX_WORD_COUNT)]

    def summarize(self):
        result = ""

        for chunk in self.text:
            response = requests.post(self.API_URL, json={'para': chunk, 'ratio': self.RATIO, 'type': 'abs'})
            response.raise_for_status()
            result += response.json()['data']['summary'] + '\n'

        return result