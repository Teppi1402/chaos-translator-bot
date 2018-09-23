import os, re, json
from datetime import datetime, date, timedelta
from flask import Flask, request, abort
import goslate
import requests
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

gs = goslate.Goslate()

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

line_bot_api = LineBotApi('6YUtLz3LrrEPOMnxZLiZLS8lqkK6cEFIlbgqlNJ5BfwjYlV47vkbgDpanyR7UYXfFwn3+5IEvxgEIQX3SrB462J9/FrwEXO1vllaiL5jbcfU4daqLE7GIwflVOG+KXc1Bv5JquQ1fbAZlpbIASGG3AdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a43d81c39b3638058ee9e84194da780d')

@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello Translator-Bot</h1>
    <p>It is currently {time}.</p>    
    """.format(time=the_time)

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
        abort(400)

    return 'OK'

def translate_text(text): 
    lang = gs.detect(text)
    trans_text = ""
    if lang == "en":
        trans_text = gs.translate(text, 'vi')
    else:
        trans_text = gs.translate(text, 'en')
    return trans_text

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == "" or "/" in text:
        return
    else:
        translated = translate_text(event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(translated))
    

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
