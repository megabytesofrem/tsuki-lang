import sys
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
        self.builtin['echo'] = lambda x: print(x)

    def run(self, program):
        tree = self.parser.parse(program)
        
        # Transform the tree
        tree = self.transformer.transform(tree)
        self.visit(tree)

    def compare(self, kind, a, b):
        # Compare a and b and return the result

        result = True
        if kind == 'comp_eq':
            if a != b:
                result = False
        elif kind == 'comp_neq':
            if a == b:
                result = False
        elif kind == 'comp_l':
            if a > b:
                result = False
        elif kind == 'comp_g':
            if a < b:
                result = False
        elif kind == 'comp_le':
            if a >= b:
                result = False
        elif kind == 'comp_ge':
            if a <= b:
                result = False
        
        return result

    def var_assign(self, tree):
        # All variables are global in Tsuki, since it is very simple
        node = tree
        name = node.name
        val = node.value

        # Resolve any variables
        if str(val) in self.globals:
            self.globals[name] = self.globals[val]
        else:
            self.globals[name] = val

    def statement(self, tree):
        for child in tree.children:
            if isinstance(child, IfStatement):
                condition = child.condition
                block = child.if_block
                (a, b) = condition.values

                # Substitute variables if they are used in the condition
                if a in self.globals:
                    a = self.globals[a]
                if b in self.globals:
                    b = self.globals[b]

                result = self.compare(condition.kind, a, b)
                if result != True:
                    self.running = False
                else:
                    self.running = True

                if self.running:
                    # Evaluate each statement in the block
                    for statement in block:
                        self.visit_children(statement)

            elif isinstance(child, VarAssign):
                self.var_assign(child)
            elif isinstance(child, FuncCall):
                self.func_call(child)

    def func_call(self, tree):
        node = tree
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
            # When functions are added, we should check upon not finding
            # a valid builtin and replace this with a print to stderr instead
            raise error.BuiltinNotFound(name)
        

interp = TsukiInterp()

# Test the interpretor out with some scripts
interp.load_builtins()
interp.run(open('examples/manesix.tsu', 'r').read())
interp.run(open('examples/password.tsu', 'r').read())
interp.run(open('examples/toggle.tsu', 'r').read())