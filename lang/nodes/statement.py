class Statement:
    def __init__(self, kind):
        self.kind = kind

class VarAssign(Statement):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class IfStatement(Statement):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block