"""
ローカルテスト用
/test
├─ test.py
└─ chromedriver
のようにchromedriverを配置すること。
"""
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from linebot import LineTextMessage

# .envの読み込み
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
print(env_path)
load_dotenv(dotenv_path=env_path)

bot_id = os.getenv("AMAOTO_BOT_ID")
mail = os.getenv("LINE_OFFICIAL_ACCOUNT_MANAGER_EMAIL")
password = os.getenv("LINE_OFFICIAL_ACCOUNT_MANAGER_PASSWORD")

print(f"mail:{mail}\npassword:{password}")
bot = LineTextMessage(bot_id,mail,password,debug=True)
# この値は適宜変える必要がある
id = bot.get_chat_id("Cd9f9c58a7c2c38068a5b28d208b1f903","あまおとちゃんデバッグ")
print(f"ID:{id}")
