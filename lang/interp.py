from lark.visitors import Interpreter

from transform import TsukiTransform
from parser import TsukiParser

class TsukiInterp(Interpreter):
    def __init__(self):
        super().__init__()

        self.parser = TsukiParser()
        self.transformer = TsukiTransform()
        self.globals = {}

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

        print(self.globals)

interp = TsukiInterp()

# Test the interpretor out
interp.run(open('examples/variables.tsu', 'r').read())