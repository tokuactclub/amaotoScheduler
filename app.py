from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from linebot import LineBotApi
from linebot.models import TextSendMessage
import json

app = Flask(__name__)

MY_CHANNEL_ACCESS_TOKEN = ""
MY_CHANNEL_SECRET = ""

configuration = Configuration(access_token=MY_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(MY_CHANNEL_SECRET)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#line APIのハンドラーを作成
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@app.route("/test")
def test():
    msg = "test"
    line_bot_api=LineBotApi(MY_CHANNEL_ACCESS_TOKEN)
    messages=TextSendMessage(text=msg)
    line_bot_api.broadcast(messages=messages)#細かいの面倒くさいので、ブロードキャストで作成。想定はグループに追加するだけ。個人使用は考えない。
    
    return "test"

#メッセージを送信する。
@app.route("/reminder",methods=["POST"])
def reminder():
    dataa=request.get_data(as_text=True)
    print(f"data:{dataa}\ntype{type(dataa)}")
    data= json.loads(dataa)
    print(f"data:{data}\ntype{type(data)}")
    try:
        msg = data["msg"]
        line_bot_api=LineBotApi(MY_CHANNEL_ACCESS_TOKEN)
        messages=TextSendMessage(text=msg)
        line_bot_api.broadcast(messages=messages)#細かいの面倒くさいので、ブロードキャストで作成。想定はグループに追加するだけ。個人使用は考えない。
        return "ok"
    except Exception as e:
        print(f"="*30)
        print(e)
        print(f"="*30)
        return f"{e}"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        #メッセージの解析
        message = event.message.text
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=event.message.text)]
            )
        )

if __name__ == "__main__":
    app.run()