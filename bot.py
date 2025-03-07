from telegram.ext import Updater, CommandHandler
import pymongo
import os
from datetime import datetime, timedelta

# Environment Variables
TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB Connection
client = pymongo.MongoClient(MONGO_URI)
db = client["traffic_db"]
collection = db["traffic"]

def visits(update, context):
    today = datetime.utcnow()
    last_2_days = today - timedelta(days=2)
    last_3_days = today - timedelta(days=3)

    two_days_count = collection.count_documents({"timestamp": {"$gte": last_2_days}})
    three_days_count = collection.count_documents({"timestamp": {"$gte": last_3_days}})

    message = (
        f"📊 *Website Insights*\n\n"
        f"🗓 *Last 2 Days:* {two_days_count} visits\n"
        f"🗓 *Last 3 Days:* {three_days_count} visits\n"
    )

    update.message.reply_text(message, parse_mode="Markdown")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("visits", visits))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
