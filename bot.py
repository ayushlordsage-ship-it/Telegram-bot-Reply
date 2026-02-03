from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ChatPermissions
import random
import time

# ===== CONFIG =====
import os

TOKEN = os.environ.get("BOT_API_TOKEN")
ADMIN_ID = int(os.environ.get("TELEGRAM_USER_ID"))

# ===== HUMAN-LIKE AUTO REPLY =====
keywords = {
      "Good morning": ["good morning 🌞","vgm"],
      "Sojao": ["sojaoo jake"],
      "promotion": ["group & channel ka promotion karwana hai to mera bio dekho or group join karke death sage ko contact karo"],
    "Death sage": ["ha bro bolo","yes say"],
     "Sage": ["bolo brother","koi kaam hai kya abhi busy tha mai chalo ruko time nikalta hu"],
    "hi": ["Hey 😊", "Hello!", "Yo 👋"],
    "hello": ["Hi there 😎", "Hello!"],
    "bye": ["Take care ❤️", "Bye 👋", "See you soonw"],
    "help": ["Yes? How can I assist you?", "I'm here 🙂"]
}

def autoreply(update, context):
    text = update.message.text.lower()
    for k in keywords:
        if k in text:
            # Simulate human typing delay
            time.sleep(random.uniform(0.5, 2.0))
            update.message.reply_text(random.choice(keywords[k]))
            break

# ===== TAG ALL =====
def tagall(update, context):
    if update.message.chat.type not in ["group", "supergroup"]:
        update.message.reply_text("This command works only in groups.")
        return
    msg = " ".join(context.args)
    text = msg + "\n"
    for member in context.bot.get_chat(update.message.chat_id).get_members():
        if member.user.username:
            text += f"@{member.user.username} "
    update.message.reply_text(text)

# ===== GLOBAL PROMOTION =====
def promotion(update, context):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("You are not admin ❌")
        return
    msg = " ".join(context.args)
    update.message.reply_text(f"Promotion sent: {msg} ✔")

# ===== MUTE USER =====
def sagemute(update, context):
    if not update.message.chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        update.message.reply_text("You need admin rights ❌")
        return
    if not context.args:
        update.message.reply_text("Usage: /sagemute @username")
        return
    username = context.args[0].replace("@","")
    chat = update.message.chat
    for member in chat.get_members():
        if member.user.username == username:
            chat.restrict_member(member.user.id, permissions=ChatPermissions(can_send_messages=False))
            update.message.reply_text(f"{username} muted ✅")
            return
    update.message.reply_text("User not found ❌")

# ===== KICK USER =====
def sagekick(update, context):
    if not update.message.chat.get_member(update.effective_user.id).status in ["administrator", "creator"]:
        update.message.reply_text("You need admin rights ❌")
        return
    if not context.args:
        update.message.reply_text("Usage: /sagekick @username")
        return
    username = context.args[0].replace("@","")
    chat = update.message.chat
    for member in chat.get_members():
        if member.user.username == username:
            chat.kick_member(member.user.id)
            update.message.reply_text(f"{username} kicked ✅")
            return
    update.message.reply_text("User not found ❌")

# ===== BAN USER =====
def sageban(update, context):
    if update.effective_user.id != ADMIN_ID:
        update.message.reply_text("You are not admin ❌")
        return
    if not context.args:
        update.message.reply_text("Usage: /sageban @username")
        return
    username = context.args[0].replace("@","")
    chat = update.message.chat
    for member in chat.get_members():
        if member.user.username == username:
            chat.kick_member(member.user.id)
            update.message.reply_text(f"{username} banned ✅")
            return
    update.message.reply_text("User not found ❌")

# ===== BOT SETUP =====
updater = Updater(TOKEN, use_context=True)
dp = updater.dispatcher

# HANDLERS
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, autoreply))
dp.add_handler(CommandHandler("tagall", tagall))
dp.add_handler(CommandHandler("sagepromotion", promotion))
dp.add_handler(CommandHandler("sagemute", sagemute))
dp.add_handler(CommandHandler("sagekick", sagekick))
dp.add_handler(CommandHandler("sageban", sageban))

# START BOT
print("Bot is starting...")
updater.start_polling()
updater.idle()
