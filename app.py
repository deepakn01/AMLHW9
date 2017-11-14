from flask import Flask, request, render_template
import walmart as wm
import threading

app = Flask(__name__)
# app.config['DEBUG'] = True


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/results", methods=['post'])


def results():
    search_term = request.form['search']
    # threading._start_new_thread(compute)

    search_term = "basket"
    walmart = wm.Walmart()
    results = walmart.get_search_results(search_term)
    walmart.write_results(results)
    rank_res = walmart.createIndex(search_term)
    print(rank_res)

    head1 = '<h1> Search Results for: ' + search_term + '</h1><br><br>'
    tbl_start = '<table><tr><th>Product</th><th>Review</th><th>Sentiment</th><th width="200"></th></tr>'
    tbl_end = '</table>'
    tbl_data = ''
    for i, result in enumerate(rank_res):
        tbl_data = tbl_data + '<tr><td>' + rank_res[i].desc + '</td><td>' + rank_res[i].review + '</td><td>' + rank_res[
            i].sentiment + '</td><td width="200"><a href="' + rank_res[i].search_url + '">Buy Now</a></td></tr>'

    return head1 + tbl_start + tbl_data + tbl_end


# app.run(debug=True)
app.run()
