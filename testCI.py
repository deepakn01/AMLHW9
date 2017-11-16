#import walmart as wm
import metapy

if __name__ == '__main__':
    query_txt = 'basketball hoop'

    idx = metapy.index.make_inverted_index('config.toml')

    query = metapy.index.Document()
    ranker = metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=500)
    # ranker = metapy.index.DirichletPrior(mu=68)
    ev = metapy.index.IREval('config.toml')
    print("Num of docs:" + str(idx.num_docs()))
    query.content(query_txt)
    print("Query text: " + query_txt)
    f_idx = metapy.index.make_forward_index('config.toml')
    ranker = metapy.index.OkapiBM25(k1=1.0, b=0.25, k3=100)
    rocchio = metapy.index.Rocchio(f_idx, ranker, alpha=0.9, beta=1.0, k=50, max_terms=50)
    score = rocchio.score(idx, query, 10)
    results = ranker.score(idx, query, 10)
    avg_p = ev.avg_p(results, 1, 10)
    print("Query {} average precision: {}".format( 1, avg_p))
    ev.map()

    print (results)
    print(score)