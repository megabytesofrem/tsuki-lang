from nodes.expression import Expression

class FuncCall(Expression):
    def __init__(self, name, params):
        self.kind = 'func_call'
        self.name = name
        self.values = params
        self.params = params