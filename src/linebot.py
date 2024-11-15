
import time
from playwright.sync_api import sync_playwright, Playwright
from random import gauss
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
        self.debug = debug
        self.as_human = True

        self.playwright:Playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=not debug)
        if debug:
             # 英語のロケールとヘッダーを設定
            self.context = self.browser.new_context(
                locale="en-US",  # 言語設定
                extra_http_headers={"Accept-Language": "en"}  # ヘッダーで明示
            )
            self.page = self.context.new_page()
        else:
            self.page = self.browser.new_page()
        #Official Account Manager にログイン
        for _ in range(3):
            if self.login(mail_address,password):
                print("login success")
                break


    def login(self,mail_address,password):
        try:
            print("login process start")

            self.page.goto(self.BASE_URL)
            print("send login get request")

            # 指定された<a>タグが表示されるまで待機
            self.xpath_click("//a[@class='btn btn-lg btn-block btn-dark' and text()='Log in with business account']")
            print("select business account")

            # メールアドレスを入力
            self.xpath_click("//input[@name='email' and @placeholder='Email address']")
            for s in mail_address:
                self.page.keyboard.press(s,delay=self.rand_gauss()/100)
            print("input email")

            # パスワードを入力
            self.xpath_click("//input[@name='password' and @placeholder='Password']")
            for s in password:
                self.page.keyboard.press(s,delay=self.rand_gauss()/100)
            # self.page.keyboard.insert_text(password)
            print("input password")
            
            # ログインボタンが表示されるまで待機
            self.xpath_click("//button[@type='submit' and contains(text(), 'Log in')]")
            print("push login button")

            # recaptchaが出ていたら諦める
            try:
                print("re captcha check")
                loc =self.xpath("//input[@id='chatListSearchInput']")
                print(self.page.locator("xpath=//input[@id='chatListSearchInput']").wait_for(timeout=150))
                print("passed")
            except:
                print("disturbed")
                return False
            
            #tipsが表示されたら消す
            page_source = self.page.content()
            with open("test.html", "w", encoding="utf-8") as file:
                file.write(page_source)
            try:
                # ログイン後のページの処理
                self.xpath("//button[@type='button' and @class='btn btn-primary' and text()='OK']")
                print("close Tips")
            except:
                pass
            print("wait 3 sec")
            time.sleep(3)
            with open("test.html", "w", encoding="utf-8") as file:
                file.write(page_source)
            
            # reCaptureに引っかかってるかを、特定の要素が表示されているかで確かめる
            try:
                textarea = self.xpath("//input[@id='chatListSearchInput']")
                self.as_human = False
                return True
            except Exception as e:
                raise Exception("reCapture disturbed")
        except Exception as e:
            raise Exception(f"failed to login,error:{e}")
        

    def text_message(self,message:str,chat_id):
        try:
            self.page.goto(f"{self.BASE_URL}{self.bot_id}/chat/{chat_id}")
            print("selected chat group")

            #確実なアイドル時間を設ける
            time.sleep(3)

            #手動チャット応答ボタンを取得
            mode_switch_button = self.xpath('//button[@id="__test__switchChatModeButton"]')
            print("found mode_switch_button")

            # 手動チャット応答に変更
            mode_switch_button.click()
            print("click mode_switch_button")

            # 入力エリアをクリック
            input_area = self.xpath("//textarea[@class='editor-textarea p-2 overflow-y-auto text-break border-0' and @inputmode='text']")
            input_area.click()

            # テキストを入力
            input_area.fill(message)

            # Enterキーを押して送信
            input_area.press("Enter")
            
            # 自動応答に戻す
            mode_switch_button.click()

        except Exception as e:
            if mode_switch_button.text == "手動チャットを終了":
                mode_switch_button.click()
            raise Exception(f"failed to send message,error:{e}\n{self.page.content}")

    def get_chat_id(self,api_id:str,chat_name:str):
        """LINE official account manager のchat_idを取得する

        Args:
            api_id (str):
            chat_name (str): _description_
        """
        self.page.goto(f"{self.BASE_URL}{self.bot_id}")
        print("access chat home")
        # uuidによるchatメッセージから絞り込み
        try:
            self.xpath_click("//input[@id='chatListSearchInput']")
        except:
            print("couldn't find text area")
            return "miss"
        print("clicked search area")
        self.page.keyboard.insert_text(api_id)

        self.xpath_click("//i[@class='las la-search mr-1']")
        print("start search...")

        # 表示の更新を待機
        self.xpath('//*[@id="__test__message_search_title"]')
        print("end search")
        
        # 対象グループをクリック
        self.xpath_click(f'//h6[text()="{chat_name}"]')
        print("clicked group chat")

        # 現在のURLからグループIDを取得
        chat_id = self.page.url.split("/")[-1]
        return chat_id

        


    def xpath_click(self,path):
        loc = self.xpath(path)
        loc.click()

    def xpath(self,path):
        # 人間らしさを表現
        if self.as_human:
            time.sleep(self.rand_gauss(97,27)/100)
        loc = self.page.locator(f"xpath={path}")
        loc.wait_for()
        return loc
    
    def rand_gauss(self,mean=60,std=30):
        while True:
            ret = gauss(mean,std)
            if not(ret < 0 or ret < std - 3 * std or std * 3 < ret):
                return ret

    def close(self):
        """
        リソースを解放するメソッド
        """
        if self.page:
            self.page.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def __del__(self):
        """
        オブジェクトが削除される際にリソースを解放
        """
        self.close()
