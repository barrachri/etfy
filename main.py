"""
Etfy Telegram Bot
author: Christian Barra
"""
import os
import logging
import uuid
from io import BytesIO
from collections import namedtuple
from datetime import datetime

from sanic import Sanic
from sanic.response import json

import telegram
from utils import message_handling, get_averages

# Start sanic
app = Sanic()

# Start logging module
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Env
PORT = int(os.getenv("PORT", "8888"))
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Telegram bot
bot = telegram.Bot(TELEGRAM_TOKEN)


@app.route("/{}".format(TELEGRAM_TOKEN), methods=['POST'])
async def webHookTelegram(request):
    """ hook for the telegram server
    is called everytime the bot receives a message

    returns a 200 message and before that sends a message to the Telegram using the API
    """

    logger.debug(f"Request: {request.json}")
    message = message_handling(request.json)
    logger.info(f"Message: {message}")
    
    if message.message_array[0] == "/etf":
        if len(message.message_array) > 1:
            text, plt = get_averages(message)
            bot.sendMessage(chat_id=message.chat_id,
                        text=text,
                        parse_mode=telegram.ParseMode.MARKDOWN)
            if plt is not None:
                buf = BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                bot.sendPhoto(message.chat_id, photo=buf)
                buf.close()
    else:
        bot.sendMessage(chat_id=message.chat_id,
                        text="Your code is not clear",
                        parse_mode=telegram.ParseMode.MARKDOWN)

    return json({"status": True})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, workers=4)
