import walmart as wm

search_term = 'basket ball hook'
        
if __name__ == '__main__':
    wal = wm.Walmart()
    results = wal.get_search_results(search_term)
    #f = open("results/results.dat","w+")
    f = open("cranfield/cranfield.dat", "w+")
    for i, result in enumerate(results):
        f.write(results[i].desc)
        f.write(' . ')
        f.write('\n')
        #print(results[i].search_url)
        #print(results[i].review)
        #print(results[i].sentiment)
        #print(len(results))
    f.close()
