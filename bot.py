import telebot, json, os, random
from flask import Flask, request
from datetime import datetime

# ---------- ENV VARIABLES ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID  = int(os.getenv("ADMIN_ID"))
ADMIN_KEY = os.getenv("ADMIN_KEY")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # ex: https://your-webservice.onrender.com/telegram_webhook
# ----------------------------------

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)
DB = "users.json"

# ---------- HELPERS ----------
def load():
    with open(DB,"r") as f:
        return json.load(f)

def save(d):
    with open(DB,"w") as f:
        json.dump(d,f,indent=2)

# ---------- TELEGRAM HANDLERS ----------
@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(m,
"""🎡 SPIN WHEEL EVENT 🎡
1️⃣ /register
2️⃣ Wait for spin
Even winners can win again!
""")

@bot.message_handler(commands=["register"])
def register(m):
    data = load()
    uid = m.from_user.id
    username = m.from_user.username or f"user{uid}"

    if any(u["id"]==uid for u in data["users"]):
        bot.reply_to(m,"❌ Already registered")
        return

    data["users"].append({"id": uid, "username": username, "joined": str(datetime.now())})
    save(data)
    bot.reply_to(m,"✅ Registered! You are now in the wheel 🎡")

# ---------- PARTICIPANTS COUNT ----------
@bot.message_handler(commands=["participants"])
def participants_count(m):
    data = load()
    bot.reply_to(m,f"👥 Total Participants: {len(data['users'])}")

# ---------- API ENDPOINTS ----------
@app.route("/participants")
def participants():
    data = load()
    return {"users": [u["username"] for u in data["users"]]}

@app.route("/spin", methods=["POST"])
def spin():
    if request.headers.get("X-ADMIN-KEY") != ADMIN_KEY:
        return "Unauthorized", 403

    data = load()
    if not data["users"]:
        return {"error":"No users"}

    winner = random.choice(data["users"])
    text = f"""🎉 SPIN RESULT 🎉
🏆 Winner: @{winner['username']}
"""
    bot.send_message(ADMIN_ID, text)
    return {"winner": winner["username"]}

# ---------- TELEGRAM WEBHOOK ----------
@app.route("/telegram_webhook", methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "", 200

# ---------- SET WEBHOOK ----------
@app.before_first_request
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)    data = load()
 
