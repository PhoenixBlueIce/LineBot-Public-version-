#接收事件 → 丟給 router → 拿回結果 → 回 LINE

#零、先 import 需要用的模組
from __future__ import annotations    #router段用的

import json    #這是為了要看 render 的 log 增加的
import logging    #這也是為了要看 render 的 log 增加的
import os
#import configparser
from flask import Flask,request,abort    #對應的是1個request
from linebot.v3.webhooks import PostbackEvent    #因為我有postbackdata，所以會有事件要處理

from router import route_event, build_reply_text

#一、從這裡開始是重點，設定會用到的模組
from linebot.v3.webhook import WebhookHandler,Event
#這個功能據說在2025年11月改版之後已經不需要了，但這邊還是使用，避免發生錯誤。
from linebot.v3.webhooks import(
    MessageEvent,
    TextMessageContent,
    PostbackEvent,
)

from linebot.v3.exceptions import InvalidSignatureError

from linebot.v3.messaging import(
    Configuration,  #圖片
    ApiClient,  #API
    MessagingApi,   #訊息
    ReplyMessageRequest,    #回應訊息
    TextMessage #這個不能處理的就是由 Message 處理。沒有「,」的話代表結尾，沒有擴充的可能性。
)

#二、設定物件
#看 render server log 用
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
#共通
#config=configparser.ConfigParser()  #後面的 C 打成小寫就"好遊戲"了，因為 ConfigParser 是一個模組
#config.read('config.ini')

app=Flask(__name__)

# 建議用 Render 的環境變數設定：
# LINE_CHANNEL_ACCESS_TOKEN / LINE_CHANNEL_SECRET
channel_access_token = os.getenv('LINE_TOKEN', '')
channel_secret = os.getenv('LINE_SECRET', '')

if not channel_access_token or not channel_secret:
    # 讓你在 Render logs 一眼看到原因（比默默 400 好）
    app.logger.warning('Missing LINE_CHANNEL_ACCESS_TOKEN or LINE_CHANNEL_SECRET')

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

#三、連結app
@app.route('/callback', methods=['POST'])   #加入註解是為了打程式碼的時候不要報錯，因為 spyder 沒有「@」的偵錯機制，因此一定會報錯但不一定有錯。
def callback():
    signature = request.headers.get('X-Line-Signature','')
    #System logger
    body=request.get_data(as_text=True)
    app.logger.info('Request Text:'+body)

    # 只為了快速確認 event 類型（不影響流程）    
    try:
        payload = json.loads(body)
        events = payload.get("events", [])
        logger.info("events_count=%s", len(events))
        for i, e in enumerate(events):
            logger.info("event[%s].type=%s", i, e.get("type"))
            # postback 的話通常這裡會有 postback.data
            if e.get("type") == "postback":
                logger.info("event[%s].postback.data=%s", i, e.get("postback", {}).get("data"))
            # message 的話通常這裡會有 message.text
            if e.get("type") == "message":
                logger.info("event[%s].message.type=%s", i, e.get("message", {}).get("type"))
                logger.info("event[%s].message.text=%s", i, e.get("message", {}).get("text"))
    except Exception as _:
        logger.info("body is not json or parse failed (ignored)")
    #get Signature，原本的程式碼還在，只是放到下面了
    try:
        handler.handle(body,signature)
    except:
        app.logger.info('Invail signature.')    #當 channel_access_token 或 channel_secret 錯誤時才會有 Invail signature 錯誤訊息。
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_text = event.message.text

    route = route_event(event_type="text", text=user_text)
    reply_text = build_reply_text(route)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )

@handler.add(PostbackEvent)
def handle_postback(event):
    postback_data = event.postback.data  # 例如 "action=joke"

    route = route_event(event_type="postback", postback_data=postback_data)
    reply_text = build_reply_text(route)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply_text)]
            )
        )