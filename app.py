from flask import Flask, request, abort  # flask, django (網頁)

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

line_bot_api = LineBotApi('xH3Bkt6tYJBRBUiXoBTiputN3zuy8iXPD0qGCYU2P8gdVhwp/2Y5m1h/pLHZiw7J2/aTXGslcSADhpZa4rbn+l0kUYJjk1b4e20P68RNjCaoXYSJXSlJP5gIbRhXDJyXHlkmYeyJpWqw+b6cezDTiwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('fc00ebbababae16b06e9881bf8ddf903')


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