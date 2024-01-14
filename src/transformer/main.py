from lark import Transformer

class MyTransformer(Transformer):

    def __init__(self, visit_tokens: bool = True) -> None:
        self.options = {
            "list":False,
            "all":False
            }
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
    
    def delete(self,items):
        return items[0].value
    
    #コマンド毎のオプション
    ##reminder
    def reminder_date(self,items):
        self.options["remindDate"] = [items[0]]


    ##schedule

    #オプションの種類
    def option_number(self,items):
        return items[0]
    def option_list(self,items):
        self.options["list"]=True
    def option_all(self,items):
        self.options["all"]=True
        return
    
    #必要情報の定義
    def event_id(self,items):
        self.options["id"]=str(items[0].value)+"@google.com"
        return
    def num(self,items):
        return int(items[0].value)