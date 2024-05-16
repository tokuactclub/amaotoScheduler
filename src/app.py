from flask import Flask, request
import requests
import json
from src.larkParser import generateParser
from lark import exceptions
from linebot import LineTextMessage
import os
import time
GAS_URL = 'https://script.google.com/macros/s/AKfycby-2Fmm9VymDqU5cEnzadScSkmCoosUKlxhcTgPD9KjNliMpiNA8cfLQO-ZLOrzP0MOxQ/exec'
GPT_URL = 'https://gpt-bot.userlocal.jp/api/webhook/2c7e8d28'


def webhook(event,url,body=None):#bodyを少し変えたい場合body変数を使う
    method = event.method
    #url = event.url
    print(f"headersType:{type(event.headers)}")
    headers = {key: value for key, value in dict(event.headers).items() if key != 'Host'} 
    if(not body):#bodyを指定されなければeventのbodyを利用（本来の挙動）
        body = event.json

    print(f"Method: {method}Type:{type(method)}")
    print(f"URL : {url}Type:{type(url)}")
    print(f"Headers: {headers}Type:{type(headers)}")
    print(f"Body: {body}Type:{type(body)}")

    try:
        # Reconstruct headers and forward the request
        headers["Content-Type"] = "application/json;charset=utf-8"
        response = requests.request(
            method=method,
            url=url,
            headers=json.loads(json.dumps(headers)),
            json=json.loads(json.dumps(body)),
        )

        print('Forwarded Data:', response)
        print('HTTP Status Code:', response.status_code)

        return 'Data forwarded successfully', 200
    except Exception as e:
        print('Error:', e)
        return 'Failed to forward data', 500
    


app = Flask(__name__)

@app.route("/boot")
def bootServer():
    print("get server boot request")
    return "server boot"

@app.route("/",methods=['POST'])
def main():
    body=request.json
    #{'destination': 'Ud686a6755685ed53407a76dd183cc82f', 'events': [{'type': 'message', 'message': {'type': 'text', 'id': '483373867147460721', 'quoteToken': 'zpxht856GpsRq9hDkQQHe69DEQ1yxu2KVKjGEW5vs4u2_KOEOPzaaJz0pTMJ7qsNnl-97gVyimImzJrsMYcdvGe5EGMYXsRjVcNS4gSvqRuGxMyY4eedM3GZk5fV8SqfntScw6R-L4uFf-2Na6mQzQ', 'text': 'さ'}, 'webhookEventId': '01HG4354B8PBWJH9AQ74AQKCAC', 'deliveryContext': {'isRedelivery': False}, 'timestamp': 1700944580461, 'source': {'type': 'user', 'userId': 'Ue99cbbb0fb4a6cb510c2ea5f343f6715'}, 'replyToken': 'fb40266f492d4e2e8963926a593c1914', 'mode': 'active'}]}
    msg : str = body["events"][0]["message"]["text"]
    if msg.startswith("あまおとちゃん"):
        serviceURL = [GPT_URL,GAS_URL]
        for url in serviceURL:
            print(f"START ACCESS TO {url}")
            response = webhook(request,url)
            print(f"END ACCESS TO {url}\nRESPONSE:{response}")
    elif msg.startswith("ama"):
        print("==============start cmd mode===============")
        url = GAS_URL
        parser = generateParser(event=body["events"][0])
        try:
            cmd,options = parser.parse(msg)
        except exceptions as e:
            print(e)
            return e,400

        body["func"] = cmd
        body["options"] = options
        
        print(f"START ACCESS TO {url}")
        response = webhook(request,url,body)
        print(f"END ACCESS TO {url}\nRESPONSE:{response}")

    
    return "complete" ,200

@app.route("/lineBot/textMessage",methods = ['POST'])
def linebot_textMessage():
    body = request.json
    bot_id = os.getenv("AMAOTO_BOT_ID")
    mail = os.getenv("LINE_OFFICIAL_ACCOUNT_MANAGER_EMAIL")
    password = os.getenv("LINE_OFFICIAL_ACCOUNT_MANAGER_PASSWORD")
    try:
        bot = LineTextMessage(bot_id,mail,password)
        bot.text_message(body["message"],body["chat_id"])
    except Exception as e:
        print(f"Error ocurred:{e}")


if __name__ == '__main__':
    
    app.run(port=3000)
