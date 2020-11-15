# SDK   Software Development Kit --> search Line python SDK (Use Line SDK to interact with LINE)

# pip 套件管理員

# This code is to build server (伺服器)

# 架設 Server有名套件: flask and django

# 加入driving time code

import simplejson

import urllib.request

from datetime import datetime
def driving_time():
    home_coord = "24.9479878,121.374193" # Home
    work_coord = "24.7703269,121.0477070" # Work 
    API1 = "AIzaSyBZbK9PBliNN1-eMp_rj0pLQw-CLRmK8eM" # Non existing example key
    API2 = "AIzaSyCGuWMrXoGL7WgT5jTprl6nyv7AziSyraU" # Non existing example key
    url_home2work = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + home_coord + "&destinations=" + work_coord + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + API1
    url_work2home = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + work_coord + "&destinations=" + home_coord + "&mode=driving&traffic_model=best_guess&departure_time=now&language=en-EN&sensor=false&key=" + API2
    result_home2work = simplejson.load(urllib.request.urlopen(url_home2work))
    result_work2home = simplejson.load(urllib.request.urlopen(url_work2home))
    driving_time_seconds_home2work = result_home2work['rows'][0]['elements'][0]['duration_in_traffic']['text']
    driving_time_seconds_work2home = result_work2home['rows'][0]['elements'][0]['duration_in_traffic']['text']


# 加入driving time code

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,StickerSendMessage
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
    msg = event.message.text
    r = '可以換一個問題嗎?'

    if '貼圖' in msg: 
        sticker_message = StickerSendMessage(
            package_id = '11537',
            sticker_id = '52002766'
        )

        line_bot_api.reply_message(
            event.reply_token,
            sticker_message)
        return


    if msg in ['hi', 'Hi']:
        r = 'hello'
    elif  msg == '你是誰':
        r = '我是機器人'

    elif msg == 'driving time':
        driving_time()

        r = '工研院 to 三峽:'+ driving_time_seconds_work2home + ', ' + '三峽 to 工研院: ' + driving_time_seconds_home2work


    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()

