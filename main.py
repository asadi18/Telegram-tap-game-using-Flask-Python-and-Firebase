import os
from flask import Flask, request, render_template, jsonify
import telebot
from firebase_admin import credentials, firestore, initialize_app

# === Configuration ===
BOT_TOKEN = "8159907105:AAHXVNDuDwZJ1xgXAa_ocKgvkBeCGEbw5hU"
FIREBASE_CRED = "firebase.json"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# === Firebase Initialization ===
cred = credentials.Certificate(FIREBASE_CRED)
initialize_app(cred)
db = firestore.client()

# === Telegram Bot Start Command ===
@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user

    # Always use user.id as primary key!
    user_data = {
        'user_id': user.id,
        'username': user.username if user.username else "",
        'first_name': user.first_name if user.first_name else "",
        'last_name': user.last_name if user.last_name else "",
        'language_code': getattr(user, 'language_code', ''),
        'coins': 0
    }
    user_doc = db.collection('users').document(str(user.id))
    # Only create if not exists
    if not user_doc.get().exists:
        user_doc.set(user_data)

    # Update with your Cloudflare URL each time!
    webapp_url = f"https://system-documented-homework-strap.trycloudflare.com/webapp?user_id={user.id}"

    # ---- THE CORRECT WAY: Launch as Telegram Web App inside Telegram ----
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    web_app_info = telebot.types.WebAppInfo(url=webapp_url)
    keyboard.add(telebot.types.KeyboardButton("🐹 Play Tap Game", web_app=web_app_info))
    bot.send_message(
        message.chat.id,
        f"Welcome, {user_data['first_name']}! Tap 🐹 Play Tap Game below to start.",
        reply_markup=keyboard
    )

# === Flask Routes ===
@app.route('/webapp')
def webapp():
    user_id = request.args.get('user_id')
    return render_template("tap.html", user_id=user_id)

@app.route('/api/user', methods=['GET'])
def get_user():
    user_id = request.args.get('user_id')
    doc = db.collection('users').document(user_id).get()
    if not doc.exists:
        return jsonify({'error': 'User not found'}), 404
    data = doc.to_dict()
    return jsonify({
        'user_id': data.get('user_id'),
        'username': data.get('username', ''),
        'first_name': data.get('first_name', ''),
        'last_name': data.get('last_name', ''),
        'language_code': data.get('language_code', ''),
        'coins': data.get('coins', 0)
    })

@app.route('/api/tap', methods=['POST'])
def tap():
    user_id = request.json['user_id']
    user_doc = db.collection('users').document(user_id)
    doc = user_doc.get()
    if not doc.exists:
        return jsonify({'error': 'User not found'}), 404
    data = doc.to_dict()
    coins = data.get('coins', 0) + 1
    user_doc.update({'coins': coins})
    return jsonify({'coins': coins})

# === Batch Tap API to make UI faster ===
@app.route('/api/batch_tap', methods=['POST'])
def batch_tap():
    user_id = request.json['user_id']
    add_coins = int(request.json.get('add_coins', 0))
    user_doc = db.collection('users').document(user_id)
    doc = user_doc.get()
    if not doc.exists:
        return jsonify({'error': 'User not found'}), 404
    data = doc.to_dict()
    coins = data.get('coins', 0) + add_coins
    user_doc.update({'coins': coins})
    return jsonify({'coins': coins})

# === Run Flask & Bot Together ===
if __name__ == '__main__':
    import threading
    threading.Thread(target=bot.polling, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)
