from lark import Lark
from transformer.main import MyTransformer

def generateParser():
    with open("src/lark/main.lark","rb") as file:
        grammar = file.read()
    grammar=grammar.decode()

    parser = Lark(grammar=grammar,
                parser='lalr',
                transformer=MyTransformer()
    )
   
    return parser

if __name__ == "__main__":
    parser = generateParser()
    print(parser.parse("ama reminder"))