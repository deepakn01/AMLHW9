import requests
from bs4 import BeautifulSoup as BS
import re
# from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SearchResult:
    def __init__(self, search_url, desc, review, sentiment):
        self.search_url = search_url
        self.desc = desc
        self.review = review
        self.sentiment = sentiment

class Walmart:
    def __init__(self):
        self.search_url = "https://www.walmart.com/search/?query="
        self.base_url = "https://www.walmart.com"

    # url = 'https://www.walmart.com/search/?query=basket&cat_id=0'
    # url = 'https://www.walmart.com/search/?query=hanger&cat_id=0'
    # url = 'https://www.walmart.com/ip/Better-Homes-and-Gardens-Medium-Wire-Basket-with-Chalkboard-Black/24534322'
    # url = 'https://www.walmart.com/ip/Woven-Wood-Basket-Set-Multiple-Colors-4-Piece-Set/54266626?variantFieldId=actual_color'
    # url = 'https://www.walmart.com/ip/Mainstays-18-Pack-Plastic-HANGER-WHITE/27631575'

    def get_search_res(self, url):
        soup = BS(requests.get(url).text, "html.parser")
        pretty_text = soup.prettify()
        match = re.findall('"productPageUrl":"(.*?)"', pretty_text)
        return match

    def get_desc(self, url):
        soup = BS(requests.get(url).text, "html.parser")
        desc_res = soup.find(class_='about-desc').contents
        desc = ''
        for tag in desc_res:
            desc += ' ' + tag.text
        return desc

    def get_review_title(self, url):
        soup = BS(requests.get(url).text, "html.parser")
        review_all = soup.find_all(class_='review-title')
        review_title = ''
        for review in review_all:
            review_title += ' ' + review.text
        return review_title

    def get_sentiment(self, text):
        # blob = TextBlob(text)
        # return blob.sentiment.polarity
        analyzer = SentimentIntensityAnalyzer()
        return str(analyzer.polarity_scores(text))

    def get_search_results(self, search_str):
        res = list()
        surl = list()
        sdesc = list()
        sreview = list()
        ssenti = list()
        try:
            match = self.get_search_res(self.search_url + search_str)
            for link in match:
                url = self.base_url + link
               # surl.append(url)
                desc = self.get_desc(url)
               # sdesc.append(desc)
                review =  self.get_review_title(url)
               # sreview.append(review)
                sentiment = self.get_sentiment(review)
               # ssenti.append(sentiment)
               # print('link: ' + url)
               # print('desc: ' + desc)
               # print('review: ' + review)
               # print('sentiment: ' + sentiment)
                r = SearchResult(url, desc, review, sentiment)
                res.append(r)
        except:
            return res
        return res


#wm = Walmart()
#res = wm.get_search_results('basket')

#print(res)




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
