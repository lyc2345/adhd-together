import os
import requests
import sys
from flask import Flask, request, abort

from linebot import (
  LineBotApi, WebhookHandler
)
from linebot.exceptions import (
  InvalidSignatureError
)
from linebot.models import *

from crawler import *

app = Flask(__name__)

# CHANNEL_ID = str(os.environ.get('ChannelId'))
# CHANNEL_ACCESS_TOKEN = str(os.environ.get('ChannelAccessToken'))
# CHANNEL_SECRET = str(os.environ.get('ChannelSecret'))
CHANNEL_ID = '1525536848'
CHANNEL_ACCESS_TOKEN = 'iAeKwakQLMCvM+eS2x6eBjkPqjFAOfwZ45fx6JzouIh+aVVYwX44+CYwsheeHkN32nIdFin9teOIvxwKvxaLxEyPiiJyp77Owqa5Bu+uLzDMYWfI6V0wavUE4DsojdpxyRnRUUXdEiNKJUfTv5ZovwdB04t89/1O/w1cDnyilFU='
CHANNEL_SECRET = 'fb87abcf6e6b239c7a5f391aa6881583'

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route('/')

def index():
  return "<p>Hello World!</p>"

@app.route('/callback', methods=['POST'])
def callback():
  # get X-Line-Signature header value
  signature = request.headers['X-Line-Signature']
  # get request body as text
  body = request.get_data(as_text=True)
   # app.logger.info('Request body: ' + body)
   # app.logger.info('signature: ' + signature)
   # handle webhook body
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)

  return 200
# @handler.add(MessageEvent, message=TextMessage)
# def handleMessage(event):
#   print('event.reply_token: ', event.reply_token)
#   print('event.message.text: ', event.message.text)
#
#   line_bot_api.reply_message(
#     event.reply_token,
#     TextSendMessage(text=event.message.text))

@handler.add(MessageEvent, message=TextMessage)
def handleMessage(event):
  # print('event.reply_token: ', event.reply_toke
  # print('event.message.text: ', event.message.text)
  if event.message.text == "709":
    content = getBusInformation('709')
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text=content)
    )
    return 0
  # line_bot_api.reply_message(
  #   event.reply_token,
  #   TextSendMessage(text=event.message.text + text))

if __name__ == "__main__":
  app.run(debug=True)
