import os
import requests
from flask import Flask, request, abort

from linebot import (
  LineBotApi, WebhookHandler
)
from linebot.exceptions import (
  InvalidSignatureError
)
from linebot.models import (
  MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)

CHANNEL_ID = str(os.environ.get('ChannelId'))
CHANNEL_ACCESS_TOKEN = str(os.environ.get('ChannelAccessToken'))
CHANNEL_SECRET = str(os.environ.get('ChannelSecret'))


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route('/')

def index():
  return "<p>Hello World!</p>"

if __name__ == '__main__':
  app.run(debug=True)


@app.route('/callback', methods=['POST'])
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

@handler.add(MessageEvent, message=TextMessage)
def handleMessage(event):
  print('event.reply_token: ', event.reply_token)
  print('event.message.text: ', event.message.text)

  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=event.message.text))


if __name__ == "__main__":
  app.run(debug=True)
