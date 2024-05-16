from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

class LineTextMessage(object):
    def __init__(self,bot_id,mail_address,password) -> None:
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

        """
        #変数の初期化
        self.bot_id = bot_id
        self.BASE_URL  = "https://chat.line.biz/"

        #chrome driverの作成
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        #render環境に合わせたオプションを追加
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=service, options=options)
        
        #Official Account Manager にログイン
        self.login(mail_address,password)


    def login(self,mail_address,password):
        try:
            self.driver.get(self.BASE_URL)
            
            # 指定された<a>タグが表示されるまで待機
            self.xpath_click("//a[@class='btn btn-lg btn-block btn-dark' and text()='ビジネスアカウントでログイン']")
            
            # メールアドレスとパスワード入力フィールドが表示されるまで待機
            email_input = self.xpath("//input[@name='email' and @placeholder='メールアドレス']")
            
            password_input = self.xpath("//input[@name='password' and @placeholder='パスワード']")
            
            # メールアドレスとパスワードを入力
            email_input.send_keys(mail_address)
            password_input.send_keys(password)
            
            # ログインボタンが表示されるまで待機
            self.xpath_click("//button[@type='submit' and contains(text(), 'ログイン')]")
            
            #tipsが表示されたら消す
            time.sleep(3)#安定性に欠けるので、少し待機
            try:
                # ログイン後のページの処理
                self.xpath_click("//button[@type='button' and @class='btn btn-primary' and text()='OK']")
            except:
                pass
        except Exception as e:
            raise Exception(f"failed to login,error:{e}")
        

    def text_message(self,message,chat_id):
        try:
            self.driver.get(f"{self.BASE_URL}{self.bot_id}/chat/{chat_id}")

            #手動チャット応答に変更
            mode_switch_button = self.xpath('//button[@id="__test__switchChatModeButton" and @class="btn btn-sm btn-outline-light"]')
            if mode_switch_button.text == "手動チャットで対応":
                mode_switch_button.click()
            finish_code = 1
            # 入力エリアのテキストエリアを取得
            
            textarea = self.xpath("//textarea[@class='editor-textarea p-2 overflow-y-auto text-break border-0' and @inputmode='text']")
            # テキストを入力
            textarea.click()
            textarea.send_keys(message)

            # Enterキーを押して送信
            textarea.send_keys(Keys.ENTER)
            
            mode_switch_button.click()
            input()

        except Exception as e:
            input(f"error:{e}")
            if mode_switch_button.text == "手動チャットを終了":
                mode_switch_button.click()
            raise Exception(f"failed to send message,error:{e}")

    def xpath_click(self,path):
        button = WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,path))
        )
        button.click()

    def xpath(self,path):
        return WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,path))
        )
