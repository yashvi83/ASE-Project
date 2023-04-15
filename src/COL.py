from NUM import NUM
from SYM import SYM

class COL:
    
    def __init__(self,n,s) -> None:
        s = s.lstrip(" ")
        self.col = NUM(n, s) if s[0].isupper() else SYM(n, s)
        self.isIgnored  = self.col.txt.endswith("X")
        self.isKlass    = self.col.txt.endswith("!") 
        self.isGoal     = self.col.txt[-1] in ["!", "+", "-"]
        # print("Type of columns-----:_:_:_:_:_:", s[0], type(self.col))