import os
import pymongo
import telebot
from datetime import datetime, timedelta

# 🔹 Telegram Bot Token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# 🔹 MongoDB Connection
MONGO_URL = "YOUR_MONGODB_CONNECTION_STRING"
client = pymongo.MongoClient(MONGO_URL)
db = client["traffic_db"]  # Database Name
collection = db["visitors"]  # Collection Name

# 🔹 Initialize Bot
bot = telebot.TeleBot(BOT_TOKEN)

# ✅ /live Command Handler
@bot.message_handler(commands=['live'])
def send_live_visitors(message):
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    visitors = collection.find({"timestamp": {"$gte": today}})  # आज के Visitors Filter

    visitor_list = []
    for visitor in visitors:
        name = visitor.get("name", "Unknown")
        country = visitor.get("country", "Unknown")
        state = visitor.get("state", "Unknown")
        visit_time = visitor["timestamp"].strftime("%H:%M:%S")  # Time in HH:MM:SS
        
        visitor_list.append(f"👤 {name} | 🌍 {country}, {state} | 🕒 {visit_time}")

    if visitor_list:
        response = "**📊 Today's Live Visitors:**\n\n" + "\n".join(visitor_list)
    else:
        response = "🚫 कोई भी Visitor अभी तक नहीं आया।"

    bot.send_message(message.chat.id, response, parse_mode="Markdown")

# 🔹 Start Bot
bot.polling()
