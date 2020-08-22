from lark import Lark
from pathlib import Path

with open('tsuki.lark', 'r') as f:
    output = f.read()    
    
parser = Lark(output, start='start')
tree = parser.parse("""
whoscool()
print(name)
print("hello world")
""")

print(tree.pretty())