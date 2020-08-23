from lark.visitors import Interpreter

from transform import TsukiTransform
from parser import TsukiParser

import error

class TsukiInterp(Interpreter):
    def __init__(self):
        super().__init__()

        self.parser = TsukiParser()
        self.transformer = TsukiTransform()
        self.globals = {}

        self.builtin = {}

    def load_builtins(self):
        self.builtin['echo'] = lambda x: print(x)

    def run(self, program):
        tree = self.parser.parse(program)
        
        # Transform the tree
        tree = self.transformer.transform(tree)
        self.visit(tree)

    def var_assign(self, tree):
        # All variables are global in Tsuki, since it is very simple
        name = tree.children[0]
        val = tree.children[1]

        # Looks complicated but if the "value" is actually a variable,
        # then use the value of the variable that it corresponds to
        if str(val) in self.globals:
            self.globals[name] = self.globals[val]
        else:
            self.globals[name] = val

    def func_call(self, tree):
        name = tree.children[0]
        params = []

        if len(tree.children) > 1:
            for child in tree.children:
                if type(child) != str:
                    param = child.children[0]
                    if param in self.globals:
                        param = self.globals[param]
                    
                    params.append(param)
        
        # Lookup the function in builtin
        if name in self.builtin:
            if len(params) > 0:
                self.builtin[name](*params)
            else:
                self.builtin[name]()
        else:
            raise error.BuiltinNotFound(name)

interp = TsukiInterp()

# Test the interpretor out
interp.load_builtins()
interp.run(open('examples/manesix.tsu', 'r').read())