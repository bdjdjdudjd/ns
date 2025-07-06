import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Menu principal
main_menu = [
    [KeyboardButton('💳 Acheter USDT'), KeyboardButton('📱 Recharger Flexy')],
    [KeyboardButton('💼 Consulter Services'), KeyboardButton('ℹ️ Aide')]
]
reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# Démarrage
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue sur le bot Multi-Services 🇩🇿 !\n\nVeuillez choisir un service dans le menu ci-dessous 👇",
        reply_markup=reply_markup
    )

# Commande d'aide
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📋 Liste des commandes disponibles :\n/start - Démarrer le bot\n/help - Obtenir de l'aide"
    )

# Gestion des messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if 'acheter usdt' in text:
        await update.message.reply_text(
            "💳 Veuillez entrer le montant en USDT que vous souhaitez acheter :"
        )
    elif 'recharger flexy' in text:
        await update.message.reply_text(
            "📱 Veuillez entrer le numéro à recharger (Djezzy, Mobilis, Ooredoo) :"
        )
    elif 'consulter services' in text:
        await update.message.reply_text(
            "💼 Services disponibles :\n- Achat USDT\n- Recharge Flexy\n- Paiement de factures\n- Autres sur demande"
        )
    elif 'aide' in text or '/help' in text:
        await help_command(update, context)
    else:
        await update.message.reply_text(
            "❓ Je n'ai pas compris votre demande. Veuillez utiliser le menu ou taper /help pour obtenir de l'aide."
        )

# Lancement du bot
def main():
    TOKEN = 'TON_TELEGRAM_BOT_TOKEN'  # Remplace par ton vrai token

    app = ApplicationBuilder().token(TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Lancer le bot
    print("✅ Bot démarré avec succès...")
    app.run_polling()

if __name__ == '__main__':
    main()
    
