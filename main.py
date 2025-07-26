import os
import subprocess
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from yt_dlp import YoutubeDL

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎧 Salom! Musiqa nomini yuboring.\n"
        "👉 Masalan: `Shape of You` yoki `/mp3 Shape of You`",
        parse_mode="Markdown"
    )

# Asosiy mp3 yuklab beruvchi funksiya
async def mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Iltimos, musiqa nomini yozing.")
        return

    query = " ".join(context.args)
    await update.message.reply_text(f"🔍 Qidirilmoqda: {query}")

    try:
        # YouTube'dan mp3 olish
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'outtmpl': 'audio.%(ext)s',
        }

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch1:{query}", download=True)
            entry = info['entries'][0]
            title = entry['title']
            file_path = ydl.prepare_filename(entry)

        # ffmpeg bilan mp3 ga o‘girish
        output_file = "output.mp3"
        subprocess.run(["ffmpeg", "-y", "-i", file_path, output_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Yuborish
        with open(output_file, "rb") as audio:
            await update.message.reply_audio(audio, title=title)

        # Fayllarni o‘chirish
        os.remove(file_path)
        os.remove(output_file)

    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {e}")

# Foydalanuvchi oddiy matn yozsa ham /mp3 kabi ishlaydi
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.args = update.message.text.split()
    return await mp3(update, context)

# Botni ishga tushirish
if __name__ == '__main__':
    app = ApplicationBuilder().token("8306771778:AAG5yK3F8CKFr556hGGiilpoG9HgRYVJZfY").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("mp3", mp3))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("🎧 Bot ishga tushdi...")
    app.run_polling()
