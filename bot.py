from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('✅ Bot démarré avec succès !')

def main():
    app = ApplicationBuilder().token('7965004321:AAEjt1sIQc8XbqK1HoDNIbo7hvn2qxj6ljI').build()
    app.add_handler(CommandHandler('start', start))
    app.run_polling()

if __name__ == '__main__':
    main()
    
