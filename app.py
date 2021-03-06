from flask import Flask, request, render_template, redirect, session, g
import walmart as wm
import kohls as kh
import rank

app = Flask(__name__)

app.config['SECRET_KEY'] = 'e5ac358c-f0bf-11e5-9e39-d3b532c10a28'

search_res = []


@app.route("/", methods=['get', 'post'])
def index():
    global search_res
    return render_template('index.html')


@app.route("/results", methods=['get', 'post'])
def results():
    global search_res
    query_txt = request.form['search']
    session['query_txt'] = query_txt
    rank.Rank.deletefile()
    walmart = wm.Walmart()
    search_res = walmart.get_search_results(query_txt)

    kohls = kh.Kohls()
    search_res.extend(kohls.get_search_results(query_txt))

    rank.Rank.write_results(search_res)
    inv_idx = rank.Rank.create_inv_idx()

    query = rank.Rank.create_query_obj(query_txt)

    ranker = rank.Rank.get_ranker(query, inv_idx)
    rank_res = ranker.score(inv_idx, query, 30)

    result = []

    for res in rank_res:
        if res[0] < len(search_res):
            result.append(res)

    print("After BM25 ranking")
    print(result)

    print(rank_res)
    rocchio_res = rank.Rank.get_rocchio_ranking(query, ranker, inv_idx)
    print(rocchio_res)

    return render_template("results.html", results=result, query_txt=query_txt, search_res=search_res)


    print(len(search_res))
    print(len(results))
    print(())

    for i, result in enumerate(results):
        print(result[0])
        print(i)
        print(search_res[i].title)

    return render_template("results.html", results = results, query_txt = query_txt, search_res = search_res)


@app.route("/rocchio/<i>/<path:u>", methods=['get', 'post'])
def rocchio_write(i, u):
    print(request.method)
    print("Link is clicked")
    print(i)
    rank.Rank.write_rocchio_feedback(i)
    print(u)
    return redirect(u)


@app.route("/rocchioresults/", methods=['get', 'post'])
def rocchioresults():
    global search_res
    query_txt = session['query_txt']
    inv_idx = rank.Rank.create_inv_idx()
    query = rank.Rank.create_query_obj(query_txt)
    ranker = rank.Rank.get_ranker(query_txt, inv_idx)
    rank_res = rank.Rank.get_rocchio_ranking(query, ranker, inv_idx)
    result = []

    for res in rank_res:
        if res[0] < len(search_res):
            result.append(res)

    print("After rocchio feedback")
    print(result)
    return render_template("rocchioresults.html", results=result, query_txt=query_txt, search_res=search_res)


app.run()
