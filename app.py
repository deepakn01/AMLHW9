from flask import Flask, request, render_template
import walmart as wm
import createIndex as ci

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def index():
    return render_template('index.html')

#test
# @app.route("/results", methods=['post'])
# def results():
#	search_term = request.form['search']
#	return render_template('results.html',s_t = search_term)


@app.route("/results", methods=['post'])
def results():
    print('hi')
    search_term = request.form['search']
    print(search_term)
    wal = wm.Walmart()
    res = wal.get_search_results(search_term)
    final_res = ci.createIndex(search_term)
    final_res_id = [item[0] for item in final_res]
    results = [res[i] for i in final_res_id]
    print(len(results))
    head1 = '<h1> Search Results for: ' + search_term + '</h1><br><br>'
    # head2 = '<br>'
    tbl_start = '<table><tr><th>Product</th><th>Review</th><th>Sentiment</th><th width="200"></th></tr>'
    tbl_end = '</table>'
    tbl_data = ''
    for i, result in enumerate(results):
        # head2 = head2+'<h2>' +result+ '&nbsp&nbsp&nbsp&nbsp'+ sentiments[i] +'</h2>'
        tbl_data = tbl_data + '<tr><td>' + results[i].desc + '</td><td>' + results[i].review + '</td><td>' + results[
            i].sentiment + '</td><td width="200"><a href="' + results[i].search_url + '">Buy Now</a></td></tr>'

    return head1 + tbl_start + tbl_data + tbl_end


app.run(debug=True)
