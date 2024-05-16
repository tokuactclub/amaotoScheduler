import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import asyncio


class LineTextMessage:
    def __init__(self, bot_id, mail_address, password):
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
        self.mail_address = mail_address
        self.password = password
        self.driver = None

    async def __aenter__(self):
        #chrome driverの作成
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        #render環境に合わせたオプションを追加
        options.add_argument('--no-sandbox')
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=service, options=options)
        
        #Official Account Manager にログイン
        await self.login()

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.driver:
            self.driver.quit()

    async def login(self):
        try:
            print("login process start")
            self.driver.get(self.BASE_URL)
            print("send login get request")

            # 指定された<a>タグが表示されるまで待機
            await self.xpath_click("//a[@class='btn btn-lg btn-block btn-dark' and text()='Log in with business account']")
            print("select business account")

            # メールアドレスとパスワード入力フィールドが表示されるまで待機
            email_input = await self.xpath("//input[@name='email' and @placeholder='Email address']")
            await email_input.send_keys(self.mail_address)
            print("input email")
            # メールアドレスとパスワードを入力
            password_input = await self.xpath("//input[@name='password' and @placeholder='Password']")
            await password_input.send_keys(self.password)
            print("input password")
            
            # ログインボタンが表示されるまで待機
            await self.xpath_click("//button[@type='submit' and contains(text(), 'Log in')]")
            print("push login button")
            
            #tipsが表示されたら消す
            await asyncio.sleep(3)#安定性に欠けるので、少し待機
            try:
                # ログイン後のページの処理
                await self.xpath_click("//button[@type='button' and @class='btn btn-primary' and text()='OK']")
            except:
                pass
        except Exception as e:
            raise Exception(f"failed to login,error:{e}")

    async def text_message(self, message, chat_id):
        try:
            self.driver.get(f"{self.BASE_URL}{self.bot_id}/chat/{chat_id}")
            print("selected chat group")
            #手動チャット応答に変更
            mode_switch_button = await self.xpath('//button[@id="__test__switchChatModeButton"]')
            print("found mode_switch_button")
            text = mode_switch_button.text
            print(text)
            if mode_switch_button.text == "手動チャットで対応":
                await mode_switch_button.click()
            print("click mode_switch_button")
            # 入力エリアのテキストエリアを取得
            
            textarea = await self.xpath("//textarea[@class='editor-textarea p-2 overflow-y-auto text-break border-0' and @inputmode='text']")
            # テキストを入力
            await textarea.click()
            await textarea.send_keys(message)

            # Enterキーを押して送信
            await textarea.send_keys(Keys.ENTER)
            
            await mode_switch_button.click()

        except Exception as e:
            if mode_switch_button.text == "手動チャットを終了":
                await mode_switch_button.click()
            raise Exception(f"failed to send message,error:{e}")

    async def xpath_click(self, path):
        button = await WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
        await button.click()

    async def xpath(self, path):
        return await WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, path))
        )
