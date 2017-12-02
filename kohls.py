import requests
from bs4 import BeautifulSoup as BS
import re
import SearchResult
# from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# todo: separate topic with weightage
# todo: create interface
# todo: add desc to app display
# todo: add more reviews
# todo: use beautiful soup instead of regex

class Kohls:
    def __init__(self):
        self.search_url = "https://www.kohls.com/search.jsp?submit-search=web-regular&search="
        self.base_url = "https://www.kohls.com"

    def get_search_url(self, url):
        soup = BS(requests.get(url).text, "html.parser")
        pretty_text = soup.prettify()
        match = re.findall('"(/product.*?jsp)"', pretty_text)

        # find unique entries
        unique = []
        for entry in match:
            m = re.match('(.*?jsp)', entry)
            if(m.group() not in unique):
                unique.append(m.group())

        return unique

    def get_desc(self, soup):
        tag = soup.find("meta", attrs={"name": "description"})
        return tag["content"]

    def get_title(self, soup):
        return soup.title.string

    def get_review_title(self, soup):
        review_all = soup.find_all("span", attrs={"itemprop":"name"})
        review_title = ''
        for review in review_all:
            review_title += ' ' + review.text
        return review_title

    def get_sentiment(self, text):
        # blob = TextBlob(text)
        # return blob.sentiment.polarity
        analyzer = SentimentIntensityAnalyzer()
        return str(analyzer.polarity_scores(text))

    def get_search_results(self, search_str, count = 15):
        res = list()
        match = self.get_search_url(self.search_url + search_str)[0:count]
        for link in match:
            try:
                url = self.base_url + link
                soup = BS(requests.get(url).text, "html.parser")

                title = self.get_title(soup)
                desc = self.get_desc(soup)
                review =  self.get_review_title(soup)
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

# search_term = "nike shoes"
# wm = Kohls()
# results = wm.get_search_results(search_term)
# wm.write_results(results)
# rank_res = wm.createIndex(search_term)
# print(rank_res)

# to get the description of the product
# res = soup.find_all(class_ = re.compile('description.*body'))
# res = soup.find(class_ = re.compile('about.*desc')).contents


# to get the search results
# search_res = soup.find_all(class_ = re.compile('product.*title.*link'))
# search_res = soup.find_all("a", class_="product-title-link")
# search_res = soup.find_all(class_ = 'product-title-link')
# search_res = soup.find_all(string = 'productPageUrl')
# search_res = soup.find_all('a')


# to get the links in the search page
# for link in search_res:
#     print(link.get('href'))

# to get the title
# print soup.title.string
# print text

# search by a string
# res = soup.find_all(string = re.compile('Better'))

# from pyquery import PyQuery as pq
# name = 'basket'
# response = pq(url=url.format(name=name))
# print response
