from lark import Transformer

class MyTransformer(Transformer):

    def __init__(self, visit_tokens: bool = True) -> None:
        self.options = {}
        super().__init__(visit_tokens)

    def script(self,items):
        return items[0],self.options

    def cmd(self,items):
        return items[0].value
    
    def option(self,items):
        return 
    
    def reminder_option(self,items):
        self.options["date"] = items[0]


    
    def num(self,items):
        return int(items[0].value)