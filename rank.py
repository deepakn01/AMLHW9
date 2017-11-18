import os
import shutil
import metapy

class Rank:
    @staticmethod
    def write_results(res):
        f = open("cranfield/cranfield.dat", "w+")
        for i, result in enumerate(res):
            f.write(res[i].title + ' ' + res[i].desc)
            f.write(' . ')
            f.write('\n')
        f.close()
        return

    @staticmethod
    def get_ranking(query_txt):
        # delete indexing if it exists
        if(os.path.isdir("idx")):
            shutil.rmtree("idx")
        idx = metapy.index.make_inverted_index('config.toml')
        print('Indexing complete')
        query = metapy.index.Document()
        ranker = metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=500)
        # ranker = metapy.index.DirichletPrior(mu=68)
        print("Num of docs:" + str(idx.num_docs()))
        query.content(query_txt)
        print("Query text: " + query_txt)
        results = ranker.score(idx, query, 10)
        print('Ranking complete')
        return (results)