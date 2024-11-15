import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

import sys
import os
from pathlib import Path
import time
from dotenv import load_dotenv
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
# .envの読み込み
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
print(env_path)
load_dotenv(dotenv_path=env_path)
from playwright.sync_api import sync_playwright, Playwright

class LineTextMessage(object):
    def __init__(self,bot_id,mail_address,password):
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

    def run(self):
        with sync_playwright() as playwright:
            run(playwright)

def run(playwright: Playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()

    
    # other actions...
    print("--login process start--")
    page.goto("https://chat.line.biz/")
    loc = page.locator("xpath=//a[@class='btn btn-lg btn-block btn-dark' and text()='Log in with business account']")
    print(loc.wait_for())
    loc.click()
    print("select business account")

    page.locator("xpath=//input[@name='email' and @placeholder='Email address']").click()
    page.keyboard.insert_text(mail)

    page.locator("xpath=//input[@name='password' and @placeholder='Password']").click()
    page.keyboard.insert_text(password)

    page.locator("xpath=//button[@type='submit' and contains(text(), 'Log in')]").click()

    time.sleep(3)    
    page_source = page.content()


    # ページソースをtest.htmlとして保存
    with open("test.html", "w", encoding="utf-8") as file:
        file.write(page_source)

    browser.close()

bot_id = os.getenv("AMAOTO_BOT_ID")
mail = os.getenv("LINE_OFFICIAL_ACCOUNT_MANAGER_EMAIL")
password = os.getenv("LINE_OFFICIAL_ACCOUNT_MANAGER_PASSWORD")
    
with sync_playwright() as playwright:
    run(playwright)