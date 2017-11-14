from flask import Flask, request, render_template
import walmart as wm

app = Flask(__name__)

@app.route("/")

def index():
    return render_template('index.html')

@app.route("/results", methods=['post'])

def results():
    search_term = request.form['search']
    walmart = wm.Walmart()
    search_res = walmart.get_search_results(search_term)
    walmart.write_results(search_res)
    rank_res = walmart.createIndex(search_term)
    print(rank_res)

    head1 = '<h1> Search Results for: ' + search_term + '</h1><br><br>'
    tbl_start = '<table><tr><th>Product</th><th>Review</th><th>Sentiment</th><th width="200"></th></tr>'
    tbl_end = '</table>'
    tbl_data = ''
    for i, result in enumerate(rank_res):
        idx = result[0]
        print(idx)
        tbl_data = tbl_data + '<tr><td>' + search_res[idx].desc + '</td><td>' + search_res[idx].review + '</td><td>' + search_res[
            idx].sentiment + '</td><td width="200"><a href="' + search_res[idx].search_url + '">Buy Now</a></td></tr>'

    return head1 + tbl_start + tbl_data + tbl_end

app.run()
