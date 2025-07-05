
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import os

# Liste des services et leurs détails
services = {
    "Flexy Multi-Opérateur": "Envoyez le numéro de téléphone et le montant à recharger.",
    "Recharge Internet": "Envoyez le numéro et le type de forfait (1 Go, 5 Go, etc.).",
    "Recharge de Jeux": "Envoyez votre ID de jeu, le jeu concerné et le montant à recharger.",
    "Vente de Cartes Google Play et iTunes": "Précisez la carte souhaitée (Google Play ou iTunes) et le montant.",
    "Paiement en Ligne pour Clients": "Envoyez les détails de l'achat (site, produit, montant).",
    "Création et Gestion de Bots Telegram": "Précisez le type de bot souhaité (commande, jeu, information, etc.).",
    "Création de CV Professionnels": "Envoyez vos informations personnelles, expériences et compétences.",
    "Conception de Cartes de Visite et Flyers": "Précisez les textes et logos à inclure dans le design.",
    "Gestion de Pages Facebook": "Précisez le secteur d'activité et les objectifs de la page.",
    "Vente de Photos et Vidéos Locales": "Envoyez la description et la destination des photos/vidéos.",
    "Vente de Produits Demandés": "Précisez le produit et la quantité souhaitée.",
    "Livraison de Petits Produits": "Précisez le produit, l'adresse et le délai de livraison.",
    "Vente de USDT et Cryptomonnaies": "Envoyez la somme à acheter ou vendre, et votre moyen de paiement.",
    "Location de Comptes Streaming": "Précisez le service (Netflix, Spotify, etc.) et la durée souhaitée.",
    "Vente de Tickets d'Événements Locaux": "Précisez l'événement et le nombre de tickets souhaité.",
    "Rédaction de Lettres Administratives": "Précisez le type de lettre et les détails à inclure.",
    "Remplissage de Formulaires en Ligne": "Précisez le type de formulaire et fournissez les données complètes.",
    "Création d'E-mails Professionnels": "Envoyez le nom souhaité et l'activité de l'entreprise.",
    "Traduction de Textes": "Envoyez le texte à traduire et la langue cible.",
    "Soutien Scolaire en Ligne": "Précisez la matière, le niveau et le type de soutien souhaité."
}

# Stockage temporaire des choix des utilisateurs
user_choices = {}

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton(service, callback_data=service)] for service in services.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Bienvenue! Voici les services disponibles:', reply_markup=reply_markup)

def service_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    selected_service = query.data
    user_id = query.from_user.id

    user_choices[user_id] = selected_service

    details = services[selected_service]
    query.edit_message_text(text=f"Vous avez choisi: {selected_service}\n{details}\n\nVeuillez fournir les informations demandées.")

def handle_message(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    if user_id in user_choices:
        service = user_choices[user_id]
        user_input = update.message.text
        update.message.reply_text(f"Votre demande pour le service '{service}' a été reçue:\n{user_input}\n\nNous vous contacterons bientôt pour finaliser.")
        del user_choices[user_id]
    else:
        update.message.reply_text("Veuillez d'abord choisir un service avec la commande /start.")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(service_selection))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
