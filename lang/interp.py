from lark.visitors import Interpreter

from transform import TsukiTransform
from parser import TsukiParser

from nodes.expression import Expression
from nodes.func_call import FuncCall

import error

class TsukiInterp(Interpreter):
    def __init__(self):
        super().__init__()

        self.parser = TsukiParser()
        self.compare_success = False
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

    def statement(self, tree):
        for child in tree.children:
            if child.data == 'if_statement':
                # The next child should be the comparison
                comparison = child.children[0]
                block = child.children[1:]

                (lvalue, rvalue) = comparison.values
                if comparison.kind == 'comp_eq':
                    if lvalue == rvalue:
                        self.compare_success = True
                    else:
                        self.compare_success = False
                elif comparison.kind == 'comp_neq':
                    if lvalue != rvalue:
                        self.compare_success = True
                    else:
                        self.compare_success = False
                
                if self.compare_success:
                    # Run the block only if the comparison was successful
                    for b in block:
                        children = self.visit_children(b)
                        for child in children:
                            if type(child) == FuncCall:
                                self.func_call(b)

    def func_call(self, tree):
        node = tree.children[0]
        name = node.name
        params = []

        for param in node.params:
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
interp.run(open('examples/expr.tsu', 'r').read())