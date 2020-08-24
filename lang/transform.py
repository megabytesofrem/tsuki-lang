from lark import Transformer, Tree

from nodes.expression import Expression
from nodes.func_call import FuncCall
from nodes.statement import IfStatement, VarAssign, ForLoop

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

    def func_call(self, args):
        name = args[0]
        params = []

        for child in args[1:]:
            if type(child) == Tree:
                params.append(child.children[0])

        return FuncCall(name, params)

    def expr(self, args):
        kind = ''
        values = []
        for i in args:
            if type(i) == Tree:
                kind = str(i.data)
                
                for child in i.children:
                    print(child)
                    if child != None:
                        values.append(child)

        print(values)
        return Expression(kind, values)

    def statement(self, args):
        # or maybe this fucks up??? I DONT KNOW
        print('STMT', args)
        return args

    # def var_assign(self, args):
    #     name = args[0]
    #     value = args[1]

    #     print(name, value)

    #     # this fucks up for some reason randomly
    #     #return (name, value)
    #     return VarAssign(name, value)

    def if_statement(self, args):
        condition = args[0]
        if_block = []

        for statement in args[1:]:
            if_block.append(statement)
                
        #return IfStatement(condition, if_block)

    # def for_loop(self, args):
    #     iterator = args[0]
    #     iterable = args[1]
    #     block = []

    #     for statement in args[1:]:
    #         block.append(statement)

    #     return ForLoop(iterator, iterable, block)