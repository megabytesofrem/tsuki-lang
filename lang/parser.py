from lark import Lark

class TsukiParser:
    def __init__(self):   
        # Open the lark grammar definition
        with open('tsuki.lark', 'r') as f:
            self._lark_output = f.read()
            self._parser = Lark(self._lark_output, start='start')

    def parse(self, s):
        return self._parser.parse(s)