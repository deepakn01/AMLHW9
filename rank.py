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
    def create_inv_idx():
        # delete indexing if it exists
        if(os.path.isdir("idx")):
            shutil.rmtree("idx")
        print('Indexing complete')
        return metapy.index.make_inverted_index('config.toml')

    @staticmethod
    def create_query_obj(query_txt):
        query_obj = metapy.index.Document()
        query_obj.content(query_txt)
        return query_obj

    @staticmethod
    def get_ranker(query, inv_idx):
        print("Num of docs:" + str(inv_idx.num_docs()))
        ranker = metapy.index.OkapiBM25(k1=1.2, b=0.75, k3=500)
        return (ranker)

    @staticmethod
    def write_rocchio_feedback(idx):
        # write to the q-rels file
        f = open("cranfield-qrels.txt", "w+")
        f.write(str(idx) + " 3 3")
        f.close()

    @staticmethod
    def get_rocchio_ranking(query, ranker, inv_idx):
        # populate the rocchio ranking
        fwd_idx = metapy.index.make_forward_index('config.toml')
        rocchio = metapy.index.Rocchio(fwd_idx, ranker, alpha=0.9, beta=1.0, k=50, max_terms=50)
        results = rocchio.score(inv_idx, query, 30)
        return results

    @staticmethod
    def deletefile():
        open("cranfield-qrels.txt", "w").close()
