# -*- coding: utf-8 -*-
__author__ = 'CubexX'

import json
import logging
import requests

from storer import Storer

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

TOKEN = ''  # TG bot token
VK_TOKEN = ''  # VK access token
PUBLIC_ID = 0  # vk.com/wall<PUBLIC_ID>_...
INTERVAL = 60  # Seconds
IGNORE_TAGS = []  # ['#IGNORE', '#HASHTAGS']

# Enable logging
logging.basicConfig(format='[%(asctime)s][%(levelname)s] - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Database
storer = Storer('bot.db')


def vk(method, params):
    params['access_token'] = VK_TOKEN
    params['v'] = 5.74
    q = requests.post('https://api.vk.com/method/' + method, data=params)
    return json.loads(q.text)


def start(bot, update):
    if storer.restore('cid') is None:
        update.message.reply_text('To get started, add me to the channel\'s administrators, '
                                  'then forward any message from the channel to this dialog')


def error(bot, update, err):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, err)


def add_bot(bot, update):
    # If message from channel
    if update.message.forward_from_chat:
        _chan = update.message.forward_from_chat
        if _chan.type == 'channel':
            cid = _chan.id

            # Add channel to database if not exists
            if storer.restore('cid') is None:
                storer.store('cid', str(cid))
                bot.sendMessage(cid, 'Ready to work!')
                logger.info('Channel id is ' + str(cid))


def parse(bot, job):
    # Get last post from public group
    post = vk('wall.get', {
        'owner_id': PUBLIC_ID,
        'count': 1
    })['response']['items'][0]

    # If exists pinned post
    if post['is_pinned']:
        post = vk('wall.get', {
            'owner_id': PUBLIC_ID,
            'count': 1,
            'offset': 1
        })['response']['items'][0]

    # If post isn't ads
    if not any(x in post['text'] for x in IGNORE_TAGS):
        cid = storer.restore('cid')
        last_id = storer.restore('last')

        # First run
        if last_id is None:
            if cid:
                bot.sendMessage(cid, 'https://vk.com/wall{}_{}\n\n{}'.format(post['from_id'], post['id'], post['text']))
                storer.store('last', post['id'])
        # If exists new post
        else:
            if last_id < post['id']:
                bot.sendMessage(cid, 'https://vk.com/wall{}_{}\n\n{}'.format(post['from_id'], post['id'], post['text']))
                storer.store('last', post['id'])


def main():
    updater = Updater(TOKEN)

    dp = updater.dispatcher

    job_queue = updater.job_queue
    job_queue.run_repeating(parse, INTERVAL)

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.forwarded, add_bot))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
