from flask import Flask, request, render_template
import walmart as wm
import kohls as kh
import rank

app = Flask(__name__)

@app.route("/")

def index():
    return render_template('index.html')

@app.route("/results", methods=['post'])

def results():
    query_txt = request.form['search']
    walmart = wm.Walmart()
    search_res = walmart.get_search_results(query_txt)

    kohls = kh.Kohls()
    search_res.extend(kohls.get_search_results(query_txt))

    rank.Rank.write_results(search_res)
    inv_idx = rank.Rank.create_inv_idx()
    query = rank.Rank.create_query_obj(query_txt)

    ranker = rank.Rank.get_ranker(query, inv_idx)
    rank_res = ranker.score(inv_idx, query, 10)
    print(rank_res)

    # write the result for Rocchio fedback
    # todo: take the user click
    rank.Rank.write_rocchio_feedback(3)

    rocchio_res = rank.Rank.get_rocchio_ranking(query, ranker, inv_idx)
    print(rocchio_res)

    head1 = '<h1> Search Results for: ' + query_txt + '</h1><br><br>'
    tbl_start = '<table><tr><th>Product</th><th>Review</th><th>Sentiment</th><th width="200"></th></tr>'
    tbl_end = '</table>'
    tbl_data = ''
    for i, result in enumerate(rocchio_res):
        inv_idx = result[0]
        print(inv_idx)
        tbl_data = tbl_data + '<tr><td>' + search_res[inv_idx].title + '</td><td>' + search_res[inv_idx].review + '</td><td>' + search_res[
            inv_idx].sentiment + '</td><td width="400"><a href="' + search_res[inv_idx].search_url + '">Buy Now</a></td></tr>'

    return head1 + tbl_start + tbl_data + tbl_end

app.run()
