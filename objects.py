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

    COOKIE = 'abID=62; abIDV2=68; anonID=7093b93112f29b90; authenticated=false; premium=false; acceptedPremiumModesTnc=false; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jul+14+2024+17%3A34%3A43+GMT%2B0200+(Central+European+Summer+Time)&version=202211.1.0&isIABGlobal=false&hosts=&landingPath=https%3A%2F%2Fquillbot.com%2Fsummarize&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A0; AMP_6e403e775d=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJiNjhmNmVlOC1iZmE3LTRjYTgtOTM3Ny1mYzI1NjZmOWYyN2UlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzIwOTcwMjY3M…6f9f27e; g_state={"i_p":1721056741031,"i_l":2}; qdid=11706773635978158115; __cf_bm=_glbO3UwW2reYdKiarAM14evFxuN5Jx9PCgkLvfW.Uo-1720971282-1.0.1.1-0V2GP5GYORkd7VCdQHkhHyykItMVdf6EtuUJ_aKG7hEJqW92uziLHZw8ZSgHC6CZ7XPxnQxtup1CwRUlH1yLiQ; _sp_ses.48cd=*; _sp_id.48cd=f676bd9b-7423-425c-a6a8-4ef50351f9d5.1720970266.1.1720971306..e5729c3c-0498-42fe-bc0f-b2c83bb3acd9..ecab750b-69c0-4db8-9849-98c77ad63af5.1720970267425.11; connect.sid=s%3Aay7uvH-IjlSSJhGbab-Bo1NiI8X_9Sag.D4aAqmi9FIcb7PgytElTAxUK8vkrD8JDLhYhcjH%2FFIM'

    def __init__(self, text):
        self.text = [text[i:i + self.MAX_WORD_COUNT] for i in range(0, len(text), self.MAX_WORD_COUNT)]

    def summarize(self):
        result = ""

        cookies = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in self.COOKIE.split('; ')}

        for chunk in self.text:
            response = requests.post(
                self.API_URL,
                json={'para': chunk, 'ratio': self.RATIO, 'type': 'abs'},
                headers={
                    'Content-Type': 'application/json',
                    'User-Agent': ua.random
                },
                cookies=cookies
            )

            response.raise_for_status()
            result += response.json()['data']['summary'] + '\n'

        return result