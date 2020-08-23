from lark import Transformer

class TsukiTransform(Transformer):
    # Atoms
    def identifier(self, args):
        (i,) = args
        return str(i)

    def value(self, args):
        (v,) = args
        return v
    
    def string(self, args):
        (s,) = args
        return str(s.replace('"', ''))

    def number(self, args):
        (a,) = args
        return int(a)
        
    def array(self, args):
        return list(args)

    def table(self, args):
        tbl = {}
        for i in args:
            (k, v) = i.children
            tbl[k] = v

        return tbl