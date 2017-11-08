# Build the query object and initialize a ranker
import metapy


def createIndex(querytext):
    idx = metapy.index.make_inverted_index('config.toml')
    query = metapy.index.Document()
    #ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)
    ranker = metapy.index.DirichletPrior(mu=68)
    print(idx.num_docs())
    num_results = 10
        #query_txt = 'basketball'
    query_txt = querytext
    print('creating index complete')
    query.content(query_txt)
    print(query)
    print(query_txt)
    results = ranker.score(idx, query, num_results)
    print('ranking complete')
    return(results)
