# SDK   Software Development Kit --> search Line python SDK (Use Line SDK to interact with LINE)

# pip 套件管理員

# This code is to build server (伺服器)

# 架設 Server有名套件: flask and django

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('Y7gX3j2bgFIXbr/kBwJWxUiq4367K6qq8lJOIcA1O2l3O/2vkt4KoL4kZccepuE9h+l8ZFahZJr4GRevFD5XwiKIRvCs+ISvmPOJmuY12HJKWk2rvnThLDI4NSzV8rpzxejSs8fDdoKmfUhnUEKbWQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b2a1ebbc7b23467b5beb785c6f46f096')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()

