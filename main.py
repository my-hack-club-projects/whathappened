import json, os
from objects import ArticleList
import colorama

SITES = json.load(open(os.path.join(os.path.dirname(__file__), 'sites.json')))

def main():
    print(colorama.Fore.BLUE + "Display all headlines as they are scraped?" + colorama.Fore.RESET)
    verbose = input("y/n: ").lower().strip().startswith('y')

    print(colorama.Fore.GREEN + "Scraping headlines..." + colorama.Fore.RESET)

    for site in SITES:
        article_list = ArticleList(site, verbose)
        article_list.get_headlines()
        print(article_list)

    print(colorama.Fore.GREEN + "Done!" + colorama.Fore.RESET)

if __name__ == '__main__':
    main()