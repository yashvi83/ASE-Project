import random
import re
import config
import math
class NUM: 
    
    def __init__(self, n=0 , s="",t=[]) -> None:
        self.at = n if n else 0
        self.txt = s if s else ""
        self.n = 0
        self.hi = float('-inf')
        self.lo= float('inf')
        self.ok= True
        self.has= []
        self.w = -1 if self.txt.endswith("-") else 1
        self.mu = 0
        self.m2 = 0
        self.sd = 0

        if t:
            for x in t:
                self.add(x)
    
    def norm(self,num,n):
        # print("num.lo", num.lo)
        # print("num.hi", num.hi)
        # print("(num.hi - num.lo + 1 / float)", (num.hi - num.lo + 1 / float("inf")))
        return n if n == "?" else (n - num.lo) / (num.hi - num.lo + 1 / float("inf"))
    
    def add(self, x):
        self.n += 1
        d = x - self.mu
        self.mu += d / self.n
        self.m2 += d * (x - self.mu)
        self.sd = 0 if self.n < 2 else math.sqrt(self.m2 / (self.n - 1))