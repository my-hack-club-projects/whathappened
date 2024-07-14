import json, os
from objects import ArticleList
import colorama

SITES = json.load(open(os.path.join(os.path.dirname(__file__), 'sites.json')))

def main():
    print(colorama.Fore.BLUE + "Display all headlines?" + colorama.Fore.RESET)
    verbose = input("y/n: ").lower().strip().startswith('y')

    print(colorama.Fore.GREEN + "Scraping headlines..." + colorama.Fore.RESET)

    article_lists = []

    for site in SITES:
        article_list = ArticleList(site, verbose)
        article_list.get_headlines()
        
        print(article_list)

        article_lists.append(article_list)

    print(colorama.Fore.GREEN + "Done scraping!" + colorama.Fore.RESET)
    print(colorama.Fore.BLUE + "Summarize all headlines?" + colorama.Fore.RESET)
    summarize = input("y/n: ").lower().strip().startswith('y')

    if not summarize:
        print(colorama.Fore.GREEN + "Exiting..." + colorama.Fore.RESET)

        return
    
    print(colorama.Fore.GREEN + "Summarizing headlines..." + colorama.Fore.RESET)

    for article_list in article_lists:
        print(colorama.Fore.YELLOW + "Summary for articles from " + article_list.name + colorama.Fore.RESET)
        print(article_list.summarize())

    print(colorama.Fore.GREEN + "Done summarizing!" + colorama.Fore.RESET)

if __name__ == '__main__':
    main()