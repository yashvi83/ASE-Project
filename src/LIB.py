import math
import random
import re
import sys
import json
from pathlib import Path
import config
import csv
from COLS import COLS
from NUM import NUM


lo = float('inf') 
hi = float('-inf')

seed = 937162211
smallPositive = 1E-32
class LIB:
    def __init__(self):
        pass

    def rint(self, lo=None, hi=None):
        return math.floor(0.5 + self.rand(lo,hi))

    def rand(self,lo=None, hi=None):
        lo, hi = lo or 0, hi or 1
        global seed
        seed = (16807 * seed) % 2147483647
        return lo + (hi-lo) * seed / 2147483647

    def rnd(self, n, nPlaces = 3):
        mult = 10**(nPlaces)
        return math.floor(n * mult + 0.5) / mult   

    def coerce(self,s):
        def fun(s1):
            if s1 == "true" or s1 == "True":
                return True
            elif s1 == "false" or s1 == "False":
                return False
            else:
                return s1
        if type(s) == bool:
            return s
        try:
            result = int(s)
        except:
            try:
                result = float(s)
            except:
                result = fun(re.match("^\s*(.+)\s*$", s).string)
        return result

    def csv(self,sFilename,fun):
        with open(sFilename, mode='r') as file:
            csvFile = csv.reader(file)
            for line in csvFile:
                fun(line)
    
    def kap(self, t, fun):
        u = {}
        items = []
        if isinstance(t, list):
            items = enumerate(t)
        else:
            print("type of t",type(t))
            if(hasattr(t,"items")):
                items = t.items()
        if(type(items)!=None):
            for k, v in items:
                    v, k = fun(k, v)
                    u[k or len(u)+1] = v
        return u

    def show(self,node,what=None,cols=None,nPlaces=None,lvl=0):
        if node:
            lvl = lvl or 0
            print("|.. " * lvl, end="")
            if ("left" not in node):
                print(self.last(self.last(node["data"].rows).cells))
            else:
                print(str(int(100 * node["C"])))
            self.show(node.get("left", None), what,cols, nPlaces, lvl+1)
            self.show(node.get("right", None), what,cols,nPlaces, lvl+1)

    def oo(self,t):
        td = t.__dict__
        td['a'] = t.__class__.__name__
        td['id'] = id(t)
        print(dict(sorted(td.items())))

    def has(self, col):
        if isinstance(col.has, dict):
            col.has = dict(sorted(col.has.items(), key = lambda item: item[1]))
        else:
            col.has.sort()
        col.ok = True
        return col.has

    def per(self, t, p):
        #print("In per: ",t)
        p = math.floor((( p or .5 ) * len(t) ))
        return t[max(0, min(len(t)-1, p))]

    def mid(self, col):
        #print("In mid: ", col.has)
        return col.mode if hasattr(col, "isSym") else self.per(self.has(col), 0.5)

    def div(self, col):
        if hasattr(col, "isSym"):
            e = 0
            for n in col.has.values():
                e = e - n/col.n * math.log(n/col.n, 2)
            return e
        else:
            return (self.per(self.has(col),.9) - self.per(self.has(col), .1)) /2.58

    def stats(self, data, nPlaces = 2, fun = None, cols = None):
        cols = cols or data.cols.y
        def callBack(k, col):
            #print("In callback:",k," ," ,col.col.has)
            col = col.col
            return round((fun or self.mid)(col), nPlaces), col.txt
        tmp = self.kap(cols, callBack)
        tmp["N"] = len(data.rows)
        return tmp
    
    def settings(self,s):
        t={}
        res = re.findall("\n[\s]+[-][\S]+[\s]+[-][-]([\S]+)[^\n]+= ([\S]+)", s)
        for k,v in res:
             t[k] = self.coerce(v)
        return t
    
    def cli(self,options):
        for k,v in options.items():
            v = str(v)
            for n, x in enumerate(sys.argv):
                if x== "-" + k[0] or x == "--" + k:
                  v = (sys.argv[n + 1] if n + 1 < len(
                        sys.argv) else False) or v == "False" and "true" or v == "True" and "false"
                options[k] = self.coerce(v)
        return options
    
    def many(self,t, n):
        u = []
        for i in range(1, n + 1):
         u.append(self.any(t))
        return u

    def any(self, t):
        return t[self.rint(len(t)) - 1]
    
    
    def extend(self,range,n,s):
        range.lo = min(n,range.lo)
        range.hi = max(n,range.hi)
        self.add(range.y,s)

    def delta(self,i, other):
        global smallPositive
        e, y, z = smallPositive, i, other
        #if(y.n !=0 and z.n != 0):
        return abs(y.mu - z.mu) / (math.sqrt(e + y.sd ** 2 / (y.n+0.0000000000001) + z.sd ** 2 / (z.n+0.0000000000001)))
    
    def samples(self, t, n = None):
        u = []
        if n is None: 
            for i in range(1, len(t)): 
                u.append(random.choice(t))
        else: 
            for i in range(1, n): 
                u.append(random.choice(t))
        return u

    def cliffsDelta(self,ns1, ns2):

        if len(ns1) > 256:
            ns1 = self.many(ns1, 256)

        if len(ns2) > 256:
            ns2 = self.many(ns2, 256)

        if len(ns1) > 10 * len(ns2):
            ns2 = self.many(ns1, 10 * len(ns2))

        if len(ns2) > 10 * len(ns1):
            ns2 = self.many(ns2, 10 * len(ns1))

        n, gt, lt = 0, 0, 0

        for _,x in enumerate(ns1):
            for _,y in enumerate(ns2):

                n = n + 1
                if x > y: gt = gt + 1 
                if x < y: lt = lt + 1

        return abs(lt - gt)/n <= .147
    
    def bootstrap(self, y0, z0):
        x, y, z, yhat, zhat = NUM(), NUM(), NUM(), [], []
        for y1 in y0:
            NUM.add(x, y1)
            NUM.add(y, y1)
        for z1 in z0:
            NUM.add(x, z1)
            NUM.add(z, z1)
        xmu, ymu, zmu = x.mu, y.mu, z.mu
        for y1 in y0: 
            yhat.append(y1 - ymu + xmu)
        for z1 in z0: 
            zhat.append(z1 - zmu + xmu)

        tobs = self.delta(y, z)
        #print("tobs",tobs)
        n = 0
        for i in range(config.the['bootstrap']):
            if (self.delta(NUM(t=self.samples(yhat)), NUM(t=self.samples(zhat))) > tobs):
                n = n + 1
        #print("after boot", n)
        return n / config.the['bootstrap'] >= config.the['conf']


    def better(self,data, row1, row2):

        s1, s2, ys = 0, 0, data.cols.y
        for col in ys:
            n1 =  float(row1[col.col.at]) if row1[col.col.at] != "?" else row1[col.col.at]
            n2 = float(row2[col.col.at]) if row2[col.col.at] != "?" else row2[col.col.at]
            x = NUM.norm(NUM,col.col, n1)
            y = NUM.norm(NUM,col.col, n2)

            s1 -= math.exp(col.col.w * (x-y)/len(ys))
            s2 -= math.exp(col.col.w * (y - x)/len(ys))

        return s1/len(ys) < s2 / len(ys)
    

    def betters(self,data,n):
        tmp=sorted(data.rows, key=lambda row: self.better(data,row, data.rows[data.rows.index(row)-1]))
        return  n and tmp[0:n], tmp[n+1:]  or tmp

    def diffs(self,nums1, nums2):
        def kap(nums, fun):
            return [fun(k, v) for k, v in enumerate(nums)]
        return kap(nums1, lambda k, nums: (self.cliffsDelta(nums.col.has, nums2[k].col.has), nums.col.txt))
    

    def value(self,has, nB = 1, nR = 1, sGoal = True,b=0,r=0):
        b,r = 0,0
        for x, n in has.items():
            if x == sGoal:
                b += n
            else:
                r += n
        b,r = b/(nB+1/float("inf")), r/(nR+1/float("inf"))
        return (b ** 2) / (b + r)