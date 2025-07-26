from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from yt_dlp import YoutubeDL
import os

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎧 Salom! Qoshiq nomini yuboring, men sizga MP3 formatda olib beraman.")

# Qoshiq nomi yuborilganda
async def get_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    await update.message.reply_text("🔍 Qidirilyapti...")

    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            filename = ydl.prepare_filename(info['entries'][0])
            mp3_file = filename.replace(".webm", ".mp3").replace(".m4a", ".mp3")

        # Audio faylni yuborish
        with open(mp3_file, 'rb') as audio:
            await update.message.reply_audio(audio, title=info['entries'][0]['title'])

        os.remove(mp3_file)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")

# Botni ishga tushurish
if __name__ == '__main__':
    app = ApplicationBuilder().token("8306771778:AAG5yK3F8CKFr556hGGiilpoG9HgRYVJZfY").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_music))

    print("🎧 Bot ishga tushdi...")
    app.run_polling()
