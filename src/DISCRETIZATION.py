from copy import deepcopy
import math
from COL import COL
import UPDATE as update
from RANGE import *
from LIB import LIB
import UPDATE as update
import config
import RULE as RULE
lib = LIB()

def is_float(element: any) -> bool:

    if element is None: 
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False

def bins(cols, Rows):
    res = []
    for col in cols:
        ranges = {}
        for y, rows in Rows.items():
            for row in rows:
                #print("row in bins:",row)
                if (isinstance(col, COL)):
                    col = col.col
                x = row[col.at]
                if x != "?" and is_float(x):
                    k = bin(col, x if x != "?" else x)
                    ranges[k] = ranges[k] if k in ranges else RANGE(col.at, col.txt, x)
                    update.extend(ranges[k], x, y)
        ranges = {key: value for key, value in sorted(ranges.items(), key=lambda x: x[1].lo)}
        newRanges = {}
        i = 0
        for key in ranges:
            newRanges[i] = ranges[key]
            i += 1
        newRangesList = []
        if hasattr(col, "isSym") and col.isSym:
            for item in newRanges.values():
                newRangesList.append(item)
        res.append(newRangesList if hasattr(col, "isSym") and col.isSym else merges(newRanges))
    return res

def bin(col, x):

    if x=="?" or hasattr(col, "isSym"):
        return x
    tmp = (col.hi - col.lo)/(config.the["bins"] - 1)
    return 1 if col.hi == col.lo else math.floor(float(x) / tmp + 0.5) * tmp


def merges(ranges0):
    def noGaps(t):
        for j in range(1, len(t)):
            t[j].lo = t[j-1].hi
        t[0].lo = -float("inf")
        t[len(t)-1].hi = float("inf")
        return t
    ranges1, j = [], 0
    while j < len(ranges0):
        left, right = ranges0[j], ranges0[j+1] if j + 1 < len(ranges0) else None
        if right:
            y = merged(left.y, right.y)
            if y:
               j = j+1
               left.hi, left.y = right.hi, y
        ranges1.append(left)
        j += 1
    return noGaps(ranges0) if len(ranges1)==len(ranges0) else merges(ranges1)


def merged(col1, col2):
    new = merge(col1, col2)
    if lib.div(new) <= (lib.div(col1)*col1.n + lib.div(col2)*col2.n)/new.n:
        return new
    

def merge(col1, col2):
    new = deepcopy(col1)
    if hasattr(col1, "isSym") and col1.isSym:
        for x, n in col2.has.items():
            update.add(new, x, n)
    else:
        for n in col2.has:
            update.add(new, n)
        new.lo = min(col1.lo, col2.lo)
        new.hi = max(col1.hi, col2.hi)
    return new


def xpln(data, best, rest):
    def v(has):
        return lib.value(has, len(best.rows), len(rest.rows), "best")
    def score(ranges):
        rule = RULE.ruleF(ranges, maxSizes)
        if rule:
            #print(showRule(rule))
            bestr= selects(rule, best.rows)
            restr= selects(rule, rest.rows)
            if len(bestr) + len(restr) > 0:
                return v({"best": len(bestr), "rest": len(restr)}), rule
    tmp, maxSizes = [], {}
    #print("res:",bins(data.cols.x, {"best": best.rows, "rest": rest.rows}))
    for ranges in bins(data.cols.x, {"best": best.rows, "rest": rest.rows}):
        if(len(ranges)!=0):
            maxSizes[ranges[0].txt] = len(ranges)
            #print("")
            for range in ranges:
                if(hasattr(range,"txt")):
                    #print(range.txt, range.lo, range.hi)
                    tmp.append({"range": range, "max": len(ranges), "val": v(range.y.has)})
    
    rule, most = firstN(sorted(tmp, key=lambda x: x["val"], reverse=True), score)
    return rule, most


def firstN(sortedRanges, scoreFun):
    if(len(sortedRanges)!=0):
        # for r in sortedRanges:
        #     print(r["range"].txt, r["range"].lo, r["range"].hi, round(r["val"], 2), r["range"].y.has)
        first = sortedRanges[0]["val"]
    def useful(range):
        if range["val"] > 0.05 and range["val"] > first / 10:
            return range

    sortedRanges = list(filter(useful, sortedRanges))
    most, out = -1, None

    for n in range(len(sortedRanges)):
        tmp, rule = scoreFun([r["range"] for r in sortedRanges[:n + 1]]) or (None, None)

        if tmp and tmp > most:
            out, most = rule, tmp

    return out, most

def showRule(rule):
    def pretty(range):
        return range['lo'] if range['lo'] == range['hi'] else [range['lo'], range['hi']]

    def merges(attr, ranges):
        return list(map(pretty, merge(sorted(ranges, key=lambda r: float(r['lo']))))), attr

    def merge(t0):
        t, j = [], 0
        while j < len(t0):
            left, right = t0[j], t0[j+1] if j+1 < len(t0) else None
            if right and left['hi'] == right['lo']:
                left['hi'] = right['hi']
                j += 1
            t.append({'lo': left['lo'], 'hi': left['hi']})
            j += 1
        return t if len(t0) == len(t) else merge(t)
    return lib.kap(rule, merges)


def selects(rule, rows):
    def disjunction(ranges, row):
        if(type(ranges)!=None):
            try:
                for range in ranges:
                        lo = int(float(range['lo'])) if isinstance(range['lo'], str) else range['lo']
                        hi = int(float(range['hi'])) if isinstance(range['hi'], str) else range['hi']
                        at = int(float(range['at']))
                        x = row[at]
                        if x == "?":
                            return True
                        x = float(x)
                        if lo == hi and lo == x:
                            return True
                        if lo <= x and x < hi:
                            return True
            except:
                print("")
        return False

    def conjunction(row):
        if(hasattr(rule,"values")):
            for ranges in rule.values():
                if not disjunction(ranges, row):
                    return False
        return True

    return [r for r in rows if conjunction(r)]