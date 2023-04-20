from DATA import DATA
from LIB import LIB
import config
lib = LIB()
def sway(data):
    def worker(rows, worse, evals0, above = None):
        #print("rows",rows)
        if len(rows) <= len(data.rows) ** config.the['min']:
            return rows, lib.many(worse, config.the['rest']*len(rows)), evals0
        else:
            l , r, A, B, c, evals = data.half(data, rows, None, above)
            if lib.better(data, B, A):
                l, r, A, B = r, l, B, A
            for row in r:
                worse.append(row)
            return worker(l, worse, evals + evals0, A)
    best, rest, evals = worker(data.rows, [], 10)
    return DATA(data, best), DATA(data, rest), evals



def sway_kmeans(data, cols=None):
    
    def worker_sway2(rows, worse):
        #print("data rows",rows)
        if len(rows) <= len(data.rows) ** config.the['min']:
            return rows, lib.many(worse, config.the['rest'] * len(rows))
        else:
            l, r, A, B = data.half_kmeans(data,rows, cols)
            #l , r, A, B, c, evals = data.half(data, rows, None, above)
            if lib.better(data,B, A):
                l, r, A, B = r, l, B, A
            for x in r:
                worse.append(x)
            return worker_sway2(l, worse)
    #print("data rows",data.rows)
    best, rest = worker_sway2(data.rows, [])
    return DATA(data, best), DATA(data, rest)