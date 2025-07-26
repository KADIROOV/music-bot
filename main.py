from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from yt_dlp import YoutubeDL
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 Salom! Qo‘shiq nomini yozing — men chiqishini ta’minlayman.")

async def music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text(f"🔍 Qidirilyapti: {query}")

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)
            entry = info['entries'][0]
            filename = ydl.prepare_filename(entry).rsplit('.', 1)[0] + '.mp3'

        with open(filename, 'rb') as audio:
            await update.message.reply_audio(audio, title=entry.get('title', query))

        os.remove(filename)

    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token("8306771778:AAG5yK3F8CKFr556hGGiilpoG9HgRYVJZfY").build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, music))

    print("✅ Bot ishga tushdi …")
    app.run_polling()
