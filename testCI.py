import createIndex as ci

search_term = 'basketball'

if __name__ == '__main__':
        #CI = ci.createIndex()
        res = ci.createIndex(search_term)
        res2 = [item[0] for item in res]
        print(res2)