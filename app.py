import os, re, json
from datetime import datetime, date, timedelta
from flask import Flask, request, abort
from googletrans import Translator
import requests
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
)

app = Flask(__name__)
translator = Translator()

channel_secret = os.getenv('e4881dd59268051feae22f38584cded1', None)
channel_access_token = os.getenv('xV4mgKpwcK4p1fOCAdOH2IXFmyRgClO+oaG7+xtWsd8x9ZrVCWifmwOYtm+k6s1JFwn3+5IEvxgEIQX3SrB462J9/FrwEXO1vllaiL5jbce+6Ce2WEJDwhY8vWwr46wgs0CADAq/RLxrDRtDjlU9jQdB04t89/1O/w1cDnyilFU=', None)

line_bot_api = LineBotApi('xV4mgKpwcK4p1fOCAdOH2IXFmyRgClO+oaG7+xtWsd8x9ZrVCWifmwOYtm+k6s1JFwn3+5IEvxgEIQX3SrB462J9/FrwEXO1vllaiL5jbce+6Ce2WEJDwhY8vWwr46wgs0CADAq/RLxrDRtDjlU9jQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e4881dd59268051feae22f38584cded1')

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
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def translate_text(text):   
    if text.startswith('/'):
        return none
    else:
        lang=translator.detect(text).lang
        if lang=='en':
            en_text = translator.translate(text, dest='vi').text
            return en_text
        else:
            en_text = translator.translate(text, dest='en').text
            return en_text

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text       
    carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URIAction(label='Go to line.me', uri='https://line.me'),
                PostbackAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackAction(label='ping with text', data='ping', text='ping'),
                MessageAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=True)
