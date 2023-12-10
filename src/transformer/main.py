from lark import Transformer

class MyTransformer(Transformer):

    def __init__(self, visit_tokens: bool = True) -> None:
        self.options = {}
        super().__init__(visit_tokens)

    def script(self,items):
        return items[0],self.options

    def cmd(self,items):
        return items[0]
    
    #コマンド
    
    def reminder(self,items):
        return  items[0].value
    
    def schedule(self,items):
        return items[0].value
    
    #コマンド毎のオプション
    ##reminder
    def reminder_date(self,items):
        self.options["date"] = items[0]

    ##schedule

    #オプションの種類
    def option_number(self,items):
        return items[0]
    
    #よみこみ
    
    def num(self,items):
        return int(items[0].value)