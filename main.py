from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import json
from ppl import manage_unread_messages

from private import TOKEN, BOT_USERNAME
from config import *


# Command section
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('active-users.json', 'r', encoding='utf-8') as f:
        active_users = json.load(f)
    with open('all-users.json', 'r', encoding='utf-8') as f:
        all_users = json.load(f)

    chat_id = update.message.chat_id
    if chat_id not in all_users:
        all_users[chat_id] = {
            'type': update.message.chat.type,
            'username': update.message.chat.username,
            'bio': update.message.chat.bio,
            'birthdate': update.message.chat.birthdate,
            'first-name': update.message.chat.first_name,
            'last-name': update.message.chat.last_name}

    with open('all-users.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(all_users, indent=4))

    if chat_id not in active_users:
        await update.message.reply_text(HAVE_NEVER_BEEN_START_MESSAGE)
    else:
        await update.message.reply_text(DEFAULT_START_MESSAGE)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE)


async def add_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('active-users.json', 'r', encoding='utf-8') as f:
        active_users = json.load(f)

    chat_id = update.message.chat_id

    if chat_id not in active_users:
        active_users.append(chat_id)
        with open('active-users.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(active_users, indent=4))

        await update.message.reply_text(ADDED_USER_MESSAGE)

    else:
        await update.message.reply_text(ALREADY_ADDED_USER_MESSAGE)


async def remove_user_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    with open('active-users.json', 'r', encoding='utf-8') as f:
        active_users = json.load(f)

    chat_id = update.message.chat_id

    if chat_id in active_users:
        active_users.remove(chat_id)
        with open('active-users.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(active_users, indent=4))

        await update.message.reply_text(REMOVED_USER_MESSAGE)

    else:
        await update.message.reply_text(ALREADY_REMOVED_USER_MESSAGE)


# Response section
def handle_response(text: str) -> str:
    return 'type /help'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update}, Error: {context.error}')


# Alongside job
async def callback_minute(context: ContextTypes.DEFAULT_TYPE):
    if manage_unread_messages():
        with open('active-users.json', 'r', encoding='utf-8') as f:
            active_users = json.load(f)

        for chat_id_loop in active_users:
            await context.bot.send_message(chat_id=chat_id_loop, text=SPAM_MESSAGE)


if __name__ == '__main__':
    # debug
    print('starting')

    app = Application.builder().token(TOKEN).build()

    # Commands bind
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add', add_user_command))
    app.add_handler(CommandHandler('remove', remove_user_command))

    # Messages bind
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors bind
    app.add_error_handler(error)

    # debug
    print('polling')

    job_queue = app.job_queue

    job_minute = job_queue.run_repeating(callback_minute, interval=JOB_INTERVAL, first=JOB_FIRST)

    app.run_polling(poll_interval=POLL_INTERVAL)
