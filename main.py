from bs4 import BeautifulSoup
import requests
import pprint
import sys

def request_api_check():
    res = requests.get('https://news.ycombinator.com/?p=2')
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check your API and try again.')

request_api_check()

def infinite_generator():
    num = 1
    while True:
        yield num
        num += 1

def scan_all_pages():
    combined_list = []
    for page in infinite_generator():
        res = requests.get('https://news.ycombinator.com/?p=' + str(page))
        athing = BeautifulSoup(res.text, 'html.parser').select('.athing')

        if len(athing) != 0:
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = soup.select('.titleline>a')
            subtext = soup.select('.subtext')
            news_list = get_news(articles, subtext, page)
            combined_list += news_list
        elif len(athing) == 0:
            print(f'News sorted from page 1 to page {page-1}')
            break
        else:
            print('Warning: something went wrong.')
            break
    return combined_list

def get_news(articles, subtext, page):
    filtered = []
    for index, item in enumerate(articles):
        title = articles[index].getText()
        link = articles[index].get('href')
        vote = subtext[index].select('.score')

        if len(vote):
            point = int(vote[0].text.replace(' points', ''))
            if point > 99:
                filtered.append({'title': title,
                                 'link': link,
                                 'votes': point,
                                 'page': page})
    return filtered

def sorted_news(top_list):
    ranked = sorted(scan_all_pages(), key=lambda x: x['votes'], reverse=True)
    return ranked[:top_list]

def main():
    top_list = sys.argv[1]
    if top_list.isnumeric():
        return sorted_news(int(top_list))
    else:
        return 'Usage: python scraper.py <number of top list to be shown>'

if __name__ == '__main__':
    pprint.pprint(main())