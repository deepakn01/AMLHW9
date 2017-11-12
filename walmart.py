import requests
from bs4 import BeautifulSoup as BS
import re
# from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import metapy

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

        # find unique entries
        output = []
        for entry in match:
            if entry not in output:
                output.append(entry)

        return output

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

    def get_search_results(self, search_str, count = 7):
        res = list()
        match = self.get_search_res(self.search_url + search_str)[0:count]
        for link in match:
            try:
                url = self.base_url + link
                desc = self.get_desc(url)
                review =  self.get_review_title(url)
                sentiment = self.get_sentiment(review)
                print('link: ' + url)
                print('desc: ' + desc)
                print('review: ' + review)
                print('sentiment: ' + sentiment)
                r = SearchResult(url, desc, review, sentiment)
                res.append(r)

            except:
                continue

        return res


    def write_results(self, res):
        f = open("cranfield/cranfield.dat", "w+")
        for i, result in enumerate(res):
            f.write(res[i].desc)
            f.write(' . ')
            f.write('\n')
        f.close()
        return


    def createIndex(self, query_txt):
        idx = metapy.index.make_inverted_index('config.toml')
        print('Indexing complete')
        query = metapy.index.Document()
        # ranker = metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=500)
        ranker = metapy.index.DirichletPrior(mu=68)
        print("Num of docs:" + str(idx.num_docs()))
        query.content(query_txt)
        print("Query text: " + query_txt)
        results = ranker.score(idx, query, 1)
        print('Ranking complete')
        return (results)

# search_term = "basket ball hoop"
search_term = "basket"
wm = Walmart()
results = wm.get_search_results(search_term)
wm.write_results(results)
rank_res = wm.createIndex(search_term)
#
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
