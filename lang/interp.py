from lark.visitors import Interpreter, visit_children_decor

from transform import TsukiTransform
from parser import TsukiParser

from nodes.expression import Expression
from nodes.func_call import FuncCall
from nodes.statement import IfStatement, VarAssign

import error

class TsukiInterp(Interpreter):
    def __init__(self):
        super().__init__()

        self.parser = TsukiParser()
        self.running = True
        self.transformer = TsukiTransform()
        self.globals = {}

        self.builtin = {}

    def load_builtins(self):
        self.builtin['echo'] = lambda x: print(x, end=' ')
        self.builtin['add']  = lambda x, y: print(x + y)

    def run(self, program):
        tree = self.parser.parse(program)
        
        # Transform the tree
        tree = self.transformer.transform(tree)
        self.visit(tree)

    def var_assign(self, tree):
        # All variables are global in Tsuki, since it is very simple
        node = tree.children[0]
        name = node.name
        val = node.value

        # Looks complicated but if the "value" is actually a variable,
        # then use the value of the variable that it corresponds to
        if str(val) in self.globals:
            self.globals[name] = self.globals[val]
        else:
            self.globals[name] = val

    def statement(self, tree):
        for child in tree.children:
            if type(child) == IfStatement:
                condition = child.condition
                block = child.if_block

                (a, b) = condition.values

                # Substitute variables if they are used in the condition
                if a in self.globals:
                    a = self.globals[a]
                if b in self.globals:
                    b = self.globals[b]

                if condition.kind == 'comp_eq':
                    if a != b: 
                        self.running = False
                    self.running = True
                elif condition.kind == 'comp_neq':
                    if a == b: 
                        self.running = False
                    self.running = True
                
                #print(condition, block, a, b)

                if self.running:
                    # Evaluate each statement in the block
                    self.visit_block(block)

    def visit_block(self, block):
        for statement in block:
            for child in statement.children:
                if isinstance(child, FuncCall):
                    self.func_call(statement)
                elif isinstance(child, VarAssign):
                    self.var_assign(statement)

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