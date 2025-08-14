import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
import threading
import time

# --- CONFIG ---
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
USER_ID = 'YOUR_USER_ID'  # Or you can send to multiple users
CHECK_INTERVAL = 3600  # seconds
tracked_games = {}  # {url: {"target_price":float, "region":str}}

# --- FUNCTIONS ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Send /game <Epic Game URL> to start tracking a game.")

def game_command(update: Update, context: CallbackContext):
    if len(context.args) != 1:
        update.message.reply_text("Usage: /game <Epic Game URL>")
        return
    url = context.args[0]
    # Save URL temporarily for this user
    context.user_data['game_url'] = url
    
    # Ask region
    keyboard = [[InlineKeyboardButton("Asia", callback_data="region_Asia"),
                 InlineKeyboardButton("Europe", callback_data="region_Europe"),
                 InlineKeyboardButton("US", callback_data="region_US")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Which region are you in?", reply_markup=reply_markup)

def region_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    
    region = query.data.split("_")[1]
    url = context.user_data.get('game_url')
    
    if not url:
        query.edit_message_text("Error: No game URL found.")
        return
    
    context.user_data['region'] = region
    
    # Fetch historical offers (simplified scraping example)
    offers = fetch_historical_offers(url, region)
    context.user_data['offers'] = offers
    
    # Show offers
    keyboard = []
    for offer in offers:
        keyboard.append([InlineKeyboardButton(f"${offer}", callback_data=f"offer_{offer}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"Select target price to track in {region}:", reply_markup=reply_markup)

def offer_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    target_price = float(query.data.split("_")[1])
    
    url = context.user_data.get('game_url')
    region = context.user_data.get('region')
    
    # Activate tracking
    tracked_games[url] = {"target_price": target_price, "region": region}
    
    query.edit_message_text(f"Tracking activated for {url} in {region} at target price ${target_price}!")

def fetch_historical_offers(url, region):
    # Simplified: in production you can use IsThereAnyDeal API or scrape Epic price history
    # For demo, we return sample prices
    return [4.99, 5.99, 6.99, 7.99]

def check_prices():
    while True:
        for url, info in tracked_games.items():
            current_price = fetch_current_price(url, info['region'])
            if current_price <= info['target_price']:
                send_telegram_alert(url, current_price)
                # Remove after notification if you want one-time alert
        time.sleep(CHECK_INTERVAL)

def fetch_current_price(url, region):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    # Simplified: Epic store may change their price tag structure
    price_tag = soup.find('span', class_='css-1n5jlnt')
    if price_tag:
        price_text = price_tag.text.strip().replace('$','')
        try:
            return float(price_text)
        except:
            return None
    return None

def send_telegram_alert(url, price):
    updater.bot.send_message(chat_id=USER_ID, text=f"🔥 Price Alert! {url} is now ${price}!")

# --- MAIN ---
updater = Updater(token=TELEGRAM_TOKEN)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("game", game_command))
dispatcher.add_handler(CallbackQueryHandler(region_callback, pattern="region_"))
dispatcher.add_handler(CallbackQueryHandler(offer_callback, pattern="offer_"))

# Start background thread for price checking
threading.Thread(target=check_prices, daemon=True).start()

updater.start_polling()
updater.idle()
  
