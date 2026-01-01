import telebot, json, os, random
from flask import Flask, jsonify, request
from threading import Thread
from datetime import datetime

# ---------- ENV VARIABLES ----------
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID  = int(os.getenv("ADMIN_ID"))
ADMIN_KEY = os.getenv("ADMIN_KEY")
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
    """Returns list of usernames"""
    data = load()
    return jsonify([u["username"] for u in data["users"]])

@app.route("/spin", methods=["POST"])
def spin():
    """Admin-only spin"""
    if request.headers.get("X-ADMIN-KEY") != ADMIN_KEY:
        return "Unauthorized", 403

    data = load()
    if not data["users"]:
        return jsonify({"error":"No users"})

    winner = random.choice(data["users"])

    text = f"""🎉 SPIN RESULT 🎉
🏆 Winner: @{winner['username']}
"""
    bot.send_message(ADMIN_ID, text)

    return jsonify({"winner": winner["username"]})

# ---------- RUN BOT + API ----------
def run_bot():
    bot.infinity_polling(skip_pending=True)

if __name__ == "__main__":
    Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=10000)
