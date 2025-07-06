import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Définir les étapes du service
CHOOSING, SERVICE_DETAIL = range(2)

# Menu principal
main_menu = [
    [KeyboardButton('💳 Acheter USDT'), KeyboardButton('📱 Recharger Flexy')],
    [KeyboardButton('💼 Consulter Services'), KeyboardButton('ℹ️ Aide')]
]
reply_markup = ReplyKeyboardMarkup(main_menu, resize_keyboard=True)

# Commande /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "Bienvenue sur le bot Multi-Services 🇩🇿 !\n\nChoisissez un service ci-dessous 👇",
        reply_markup=reply_markup
    )
    return CHOOSING

# Commande /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📋 Commandes disponibles :\n/start - Démarrer le bot\n/help - Obtenir de l'aide\nVous pouvez aussi utiliser le menu directement."
    )

# Gestion des choix du menu
async def handle_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text.lower()

    if 'acheter usdt' in text:
        await update.message.reply_text("💳 Veuillez entrer le montant en USDT que vous souhaitez acheter :")
        context.user_data['service'] = 'usdt'
        return SERVICE_DETAIL

    elif 'recharger flexy' in text:
        await update.message.reply_text("📱 Veuillez entrer le numéro de téléphone à recharger :")
        context.user_data['service'] = 'flexy'
        return SERVICE_DETAIL

    elif 'consulter services' in text:
        await update.message.reply_text("💼 Services disponibles :\n- Achat USDT\n- Recharge Flexy\n- Paiement de factures\n- Autres services sur demande.")
        return CHOOSING

    elif 'aide' in text:
        await help_command(update, context)
        return CHOOSING

    else:
        await update.message.reply_text("❓ Je n'ai pas compris. Veuillez utiliser le menu ou taper /help.")
        return CHOOSING

# Gestion des informations saisies par l'utilisateur
async def handle_service_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    selected_service = context.user_data.get('service')

    if selected_service == 'usdt':
        await update.message.reply_text(f"✅ Votre demande d'achat de {user_input} USDT a été reçue. Nous vous contacterons rapidement.")
    elif selected_service == 'flexy':
        await update.message.reply_text(f"✅ Recharge Flexy pour le numéro {user_input} enregistrée. Traitement en cours.")
    else:
        await update.message.reply_text("❗ Une erreur est survenue. Veuillez recommencer.")

    return CHOOSING

# Annuler la conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("🚫 Opération annulée. Tapez /start pour recommencer.")
    return ConversationHandler.END

# Lancement du bot
def main():
    TOKEN = '7965004321:AAEjt1sIQc8XbqK1HoDNIbo7hvn2qxj6ljI'  # Remplace par ton token

    app = ApplicationBuilder().token(TOKEN).build()

    # Gestionnaire de conversation
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_choice)],
            SERVICE_DETAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_service_detail)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Ajouter les gestionnaires
    app.add_handler(conv_handler)
    app.add_handler(CommandHandler('help', help_command))

    # Lancer le bot
    print("✅ Bot démarré avec succès...")
    app.run_polling()

if __name__ == '__main__':
    main()
