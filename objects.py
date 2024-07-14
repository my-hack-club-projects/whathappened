from fake_useragent import UserAgent

import colorama
import requests
import bs4

from lexrank import LexRank
from lexrank.mappings.stopwords import STOPWORDS
from path import Path

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
    def __init__(self, text):
        self.text = text
    
    def summarize(self):
        documents = []
        documents_dir = Path('bbc/politics')

        for file_path in documents_dir.files('*.txt'):
            with file_path.open(mode='rt', encoding='utf-8') as fp:
                documents.append(fp.readlines())

        lxr = LexRank(documents, stopwords=STOPWORDS['en'])

        sentences = [sentence for sentence in self.text.split('\n') if '?' not in sentence]

        summary = lxr.get_summary(sentences, summary_size=3, threshold=2)

        return '. '.join(summary)