from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class LineTextMessage(object):
    def __init__(self,bot_id,mail_address,password,debug=False) -> None:
        """
        LINE Official Acount Managerを利用しbotからテキストメッセージを送信する
        
        Args
        ----
        bot_id:str
            利用するbotのid
            https://chat.line.biz/{bot_id}/
        mail_address:str   
            Official Acount Managerにログインするユーザーのメールアドレス
            botに対してアクセス権を持つユーザーである必要がある
        password:str
            ログインするユーザーのパスワード
        debug:bool
            ローカルで動作確認する時のためのオプション
        """
        #変数の初期化
        self.bot_id = bot_id
        self.BASE_URL  = "https://chat.line.biz/"

        #chrome driverの作成
        if not debug:
            service = Service(ChromeDriverManager().install())
            options = webdriver.ChromeOptions()
            #render環境に合わせたオプションを追加
            options.add_argument('--no-sandbox')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            self.driver = webdriver.Chrome(service=service, options=options)
        else:
            options = webdriver.ChromeOptions()
            options.add_argument('--lang=en')
            options.add_experimental_option('prefs', {'intl.accept_languages': 'en'})
            self.driver = webdriver.Chrome(options=options)
        
        #Official Account Manager にログイン
        self.login(mail_address,password)


    def login(self,mail_address,password):
        try:
            print("login process start")
            self.driver.get(self.BASE_URL)
            print("send login get request")

            # 指定された<a>タグが表示されるまで待機
            self.xpath_click("//a[@class='btn btn-lg btn-block btn-dark' and text()='Log in with business account']")
            print("select business account")

            # メールアドレスとパスワード入力フィールドが表示されるまで待機
            email_input = self.xpath("//input[@name='email' and @placeholder='Email address']")
            email_input.send_keys(mail_address)
            print("input email")
            # メールアドレスとパスワードを入力
            password_input = self.xpath("//input[@name='password' and @placeholder='Password']")
            password_input.send_keys(password)
            print("input password")
            
            # ログインボタンが表示されるまで待機
            self.xpath_click("//button[@type='submit' and contains(text(), 'Log in')]")
            print("push login button")
            
            #tipsが表示されたら消す
            time.sleep(10)#安定性に欠けるので、少し待機
            try:
                # ログイン後のページの処理
                self.xpath_click("//button[@type='button' and @class='btn btn-primary' and text()='OK']")
            except:
                pass
        except Exception as e:
            raise Exception(f"failed to login,error:{e}")
        

    def text_message(self,message:str,chat_id):
        try:
            self.driver.get(f"{self.BASE_URL}{self.bot_id}/chat/{chat_id}")
            print("selected chat group")
            #確実なアイドル時間を設ける
            time.sleep(3)
            #手動チャット応答に変更
            mode_switch_button = self.xpath('//button[@id="__test__switchChatModeButton"]')
            print("found mode_switch_button")
            if mode_switch_button.text == "手動チャットで対応":
                mode_switch_button.click()
            print("click mode_switch_button")
            # 入力エリアのテキストエリアを取得
            
            textarea = self.xpath("//textarea[@class='editor-textarea p-2 overflow-y-auto text-break border-0' and @inputmode='text']")
            # テキストを入力
            textarea.click()
            for sentence in message.split("\n"):
                textarea.send_keys(sentence)
                textarea.send_keys(Keys.LEFT_SHIFT+Keys.ENTER)
            textarea.send_keys(Keys.DELETE)

            # Enterキーを押して送信
            textarea.send_keys(Keys.ENTER)
            
            mode_switch_button.click()

        except Exception as e:
            if mode_switch_button.text == "手動チャットを終了":
                mode_switch_button.click()
            raise Exception(f"failed to send message,error:{e}\n{self.driver.page_source}")

    def get_chat_id(self,api_id:str,chat_name:str):
        """LINE official account manager のchat_idを取得する

        Args:
            api_id (str):
            chat_name (str): _description_
        """
        raise Exception("test")
        self.driver.get(f"{self.BASE_URL}{self.bot_id}")
        print("access chat home")
        # uuidによるchatメッセージから絞り込み
        textarea = self.xpath("//input[@id='chatListSearchInput']")
        if not textarea:
            print("couldn't find text area")
            return "miss"
        textarea.click()
        print("clicked search area")
        textarea.send_keys(api_id)
        self.xpath_click("//i[@class='las la-search mr-1']")
        print("start search...")

        # 表示の更新を待機
        WebDriverWait(self.driver,120).until(
            EC.presence_of_element_located((By.XPATH,'//*[@id="__test__message_search_title"]'))
        )
        print("end search")
        # 対象グループをクリック
        self.xpath_click(f'//h6[text()="{chat_name}"]')
        print("clicked group chat")
        # 現在のURLからグループIDを取得
        chat_id = self.driver.current_url.split("/")[-1]
        return chat_id

        


    def xpath_click(self,path):
        button = self.xpath(path)
        button.click()

    def xpath(self,path):
        
        return WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,path))
        )