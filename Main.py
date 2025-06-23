# bot.py

import os
import logging
from pytube import YouTube
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Setup logging (optional but useful)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ⚠️ Replace with your real token or use environment variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7850703374:AAEBF-vJwHcn6bflQCEr4pTBkvuAtubftwI")


# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Hi! Send me a YouTube video URL, and I'll download it for you.")


# Main handler to process URLs
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not ("youtube.com" in url or "youtu.be" in url):
        await update.message.reply_text("❌ Please send a valid YouTube URL.")
        return

    try:
        await update.message.reply_text("📥 Downloading the video... Please wait.")
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()

        filename = stream.download()
        logging.info(f"Downloaded video: {filename}")

        with open(filename, 'rb') as video:
            await update.message.reply_video(video=video, timeout=120)

        os.remove(filename)
        logging.info(f"Removed local file: {filename}")

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"⚠️ Failed to download video. Reason: {str(e)}")


# Run the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot is running...")
    app.run_polling()


if __name__ == '__main__':
    main()
