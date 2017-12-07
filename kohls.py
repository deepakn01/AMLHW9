import requests
import bs4
import re
import SearchResult
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Kohls:
    def __init__(self):
        self.search_url = "https://www.kohls.com/search.jsp?submit-search=web-regular&search="
        self.base_url = "https://www.kohls.com"

    def get_search_url(self, url):
        soup = bs4.BeautifulSoup(requests.get(url).text, "html.parser")
        pretty_text = soup.prettify()
        match = re.findall('"(/product.*?jsp)"', pretty_text)

        # find unique entries
        unique = []
        for entry in match:
            m = re.match('(.*?jsp)', entry)
            if (m.group() not in unique):
                unique.append(m.group())

        return unique

    def get_desc(self, soup):
        tag = soup.find("meta", attrs={"name": "description"})
        return tag["content"]

    def get_title(self, soup):
        return soup.title.string

    def get_review_title(self, soup):
        review_all = soup.find_all("span", attrs={"itemprop": "name"})
        review_title = ''
        for review in review_all:
            review_title += ' ' + review.text
        return review_title

    def get_sentiment(self, text):
        analyzer = SentimentIntensityAnalyzer()
        return str(analyzer.polarity_scores(text))

    def get_search_results(self, search_str, count=15):
        res = list()
        match = self.get_search_url(self.search_url + search_str)[0:count]
        for link in match:
            try:
                url = self.base_url + link
                soup = bs4.BeautifulSoup(requests.get(url).text, "html.parser")

                title = self.get_title(soup)
                desc = self.get_desc(soup)
                review = self.get_review_title(soup)
                sentiment = self.get_sentiment(review)
                print('link: ' + url)
                print('title: ' + title)
                print('desc: ' + desc)
                print('review: ' + review)
                print('sentiment: ' + sentiment)
                r = SearchResult.SearchResult(self.base_url, url, title, desc, review, sentiment)
                res.append(r)

            except:
                continue

        return res

## Test code
# search_term = "basket"
# kh = Kohls()
# results = kh.get_search_results(search_term)
# kh.write_results(results)
# rank_res = kh.createIndex(search_term)
# print(rank_res)
