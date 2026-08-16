# -*- coding: utf-8 -*-
import telebot
from telebot import types
import os, requests, time, threading
from flask import Flask

BOT_TOKEN = os.getenv("BOT_TOKEN", "8855823255:AAGe8a9FYnjIJTz2WWncDJ7kenDbLI4YMBE")
ADMIN_ID = 8981733976
UPI_ID = "zervicxplay@okhdfcbank"
USDT_ADDRESS = "TLwAWcJ7Tm34jqyYqV6qhizQHy8pe7US1V"
SUPPORT_LINK = "https://t.me/just_zevric"
API_KEY = os.getenv("API_KEY", "ffcc751480b3c67244ea7123acbeb608")
API_BASE = "https://premiumotp.pro/api/v1/stark"
PROFIT = 40

WEBSITE_SERVERS = {
    "Argentina server 1": 99, "Bangladesh server 1": 55, "Bangladesh server 3": 75, "Brazil": 150,
    "Canada server 14": 42, "Canada server 15": 42, "Canada server 16": 50, "Canada server 18": 99,
    "Canada server 21": 55, "Canada server 22": 53, "Canada server 3": 52, "Chile": 35,
    "Chile server 1": 28, "Chile server 2": 40, "Colombia": 35, "Colombia server 1": 55,
    "Colombia server 5": 55, "Colombia server 8": 42, "India server 10": 112, "India server 25": 120,
    "Indonesia": 28, "Indonesia server 12": 25, "Indonesia server 14": 25, "Indonesia server 15": 23,
    "Indonesia server 16": 25, "Indonesia server 17": 25, "Indonesia server 18": 25, "Indonesia server 2": 25,
    "Indonesia server 6": 33, "Indonesia server 9": 24, "Ivory Coast": 25, "Kenya server 1": 40,
    "Malaysia server 1": 85, "Malaysia server 2": 89, "Mauritania server 1": 40, "Nepal server 2": 55,
    "Netherlands": 155, "Philippines": 27, "Philippines server 3": 45, "Philippines server 5": 50,
    "Poland server 1": 90, "Saudi Arabia server 1": 60, "South Africa": 25, "South Africa server 3": 23,
    "South Africa server 6": 22, "South Africa server 7": 19, "South Africa server 8": 20,
    "Thailand server 1": 60, "Thailand server 3": 73, "USA": 115, "USA server 0": 70,
    "USA server 1": 199, "USA server 12": 28, "USA server 17": 25, "USA server 25": 60,
    "USA server 26": 40, "United Kingdom": 65, "United Kingdom server 2": 105,
    "Uzbekistan server 1": 90, "Vietnam server 1": 50, "Vietnam server 2": 35, "Yemen server 1": 22,
}
FLAGS = {
    "Argentina": "🇦🇷 +54", "Bangladesh": "🇧🇩 +880", "Brazil": "🇧🇷 +55", "Canada": "🇨🇦 +1",
    "Chile": "🇨🇱 +56", "Colombia": "🇨🇴 +57", "India": "🇮🇳 +91", "Indonesia": "🇮🇩 +62",
    "Ivory Coast": "🇨🇮 +225", "Kenya": "🇰🇪 +254", "Malaysia": "🇲🇾 +60", "Mauritania": "🇲🇷 +222",
    "Nepal": "🇳🇵 +977", "Netherlands": "🇳🇱 +31", "Philippines": "🇵🇭 +63", "Poland": "🇵🇱 +48",
    "Saudi Arabia": "🇸🇦 +966", "South Africa": "🇿🇦 +27", "Thailand": "🇹🇭 +66", "USA": "🇺🇸 +1",
    "United Kingdom": "🇬🇧 +44", "Uzbekistan": "🇺🇿 +998", "Vietnam": "🇻🇳 +84", "Yemen": "🇾🇪 +967",
}
def get_flag(s):
    for c, fc in FLAGS.items():
        if c.lower() in s.lower(): p=fc.split(" "); return p[0]," ".join(p[1:])
    return "🌍","+?"

bot=telebot.TeleBot(BOT_TOKEN)
bot.delete_webhook()
try: import qrcode; QR_OK=True
except: QR_OK=False

user_selection={}; user_numbers={}; user_activations={}; pending_orders={}

def set_commands():
    try:
        bot.delete_my_commands()
        bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
        bot.delete_my_commands(scope=types.BotCommandScopeChat(chat_id=ADMIN_ID))
    except: pass
    # Public commands - WITHOUT admin balance, so normal users cannot see
    public_cmds=[
        types.BotCommand("start","🔥 Main Menu"),
        types.BotCommand("buy","🛒 Buy Number"),
        types.BotCommand("pricelist","💰 Price List"),
        types.BotCommand("howtobuy","❓ How to Buy"),
        types.BotCommand("support","📞 Support"),
    ]
    # Admin commands - includes balance, only for admin chat
    admin_cmds=public_cmds+[
        types.BotCommand("balance","💳 Admin Balance"),
        types.BotCommand("admin","🔐 Admin Panel"),
    ]
    try:
        bot.set_my_commands(public_cmds, scope=types.BotCommandScopeAllPrivateChats())
        bot.set_my_commands(admin_cmds, scope=types.BotCommandScopeChat(chat_id=ADMIN_ID))
        print("Commands set: Public without balance, Admin with balance")
    except Exception as e: print(f"Command error: {e}")
set_commands()

def api_buy(server):
    try:
        url=f"{API_BASE}?api_key={API_KEY}&action=getNumber&service=wa&server={server}"
        r=requests.get(url,timeout=15); txt=r.text.strip()
        if "ACCESS_NUMBER" in txt: p=txt.split(":"); return {"id":p[1],"number":p[2]}
        if "NO_NUMBERS" in txt or "NO_BALANCE" in txt:
            url2=f"{API_BASE}?api_key={API_KEY}&action=getNumber&service=wa"
            r2=requests.get(url2,timeout=15); txt2=r2.text.strip()
            if "ACCESS_NUMBER" in txt2: p=txt2.split(":"); return {"id":p[1],"number":p[2]}
        return {"error":txt}
    except Exception as e: return {"error":str(e)}

def api_otp(oid):
    try:
        url=f"{API_BASE}?api_key={API_KEY}&action=getStatus&id={oid}"
        r=requests.get(url,timeout=10); txt=r.text.strip()
        if "STATUS_OK" in txt: return txt.split(":")[1]
        return None
    except: return None

def api_cancel(oid):
    try: return requests.get(f"{API_BASE}?api_key={API_KEY}&action=setStatus&id={oid}&status=8",timeout=10).text
    except: return "Error"

def api_bal():
    try: return requests.get(f"{API_BASE}?api_key={API_KEY}&action=getBalance",timeout=10).text
    except: return "Error"

def make_upi_qr(amount):
    if not QR_OK: return None
    try:
        import qrcode; upi_str=f"upi://pay?pa={UPI_ID}&pn=ZEVRIC&am={amount}&cu=INR"
        qr=qrcode.make(upi_str); path=f"/tmp/qr_upi_{amount}.png"; qr.save(path); return path
    except: return None

def make_usdt_qr():
    if not QR_OK: return None
    try: import qrcode; qr=qrcode.make(USDT_ADDRESS); path="/tmp/qr_usdt.png"; qr.save(path); return path
    except: return None

def country_menu(page=0):
    items=list(WEBSITE_SERVERS.items()); per_page=8; s=page*per_page; e=s+per_page
    mk=types.InlineKeyboardMarkup(row_width=1)
    for name,wp in items[s:e]:
        flag,code=get_flag(name); mk.add(types.InlineKeyboardButton(f"{flag} {name} {code} - ₹{wp+PROFIT} ✅", callback_data=f"c_{name}"))
    nav=[]
    if page>0: nav.append(types.InlineKeyboardButton("⬅️ Prev", callback_data=f"p_{page-1}"))
    if e<len(items): nav.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"p_{page+1}"))
    if nav: mk.row(*nav)
    mk.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main"))
    return mk

def main_kb():
    m=types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("🛒 Buy Whatsapp Number 🔥", callback_data="buy"), types.InlineKeyboardButton("💰 Price List", callback_data="pricelist"))
    m.add(types.InlineKeyboardButton("❓ How to Buy", callback_data="howtobuy"), types.InlineKeyboardButton("📞 Support", url=SUPPORT_LINK))
    return m

def after_number_kb(uid):
    oid=user_activations.get(uid,"")
    m=types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("🔑 Get OTP (Auto) - Click Here 👇", callback_data=f"go_{uid}"))
    m.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main"), types.InlineKeyboardButton("📞 Support", url=SUPPORT_LINK))
    m.add(types.InlineKeyboardButton("❌ Cancel & Refund", callback_data=f"cancel_{oid}"))
    return m

@bot.message_handler(commands=['start'])
def start_h(message):
    txt="""🔥 ZEVRIC OTP BAZAAR 🔥
━━━━━━━━━━━━━━━━━━━━
💜 Only Whatsapp - Instant Delivery 💜
━━━━━━━━━━━━━━━━━━━━
🚀 62+ Servers Available
⚡ Fast OTP - Auto Delivery
✅ Real Numbers - No Fake
📞 24/7 Support Available
━━━━━━━━━━━━━━━━━━━━
👇 Select from Menu:"""
    bot.send_message(message.chat.id, txt, reply_markup=main_kb())

@bot.message_handler(commands=['buy'])
def buy_h(m): bot.send_message(m.chat.id, "📱 SELECT SERVER - Whatsapp Only ✅\n⚡ Instant Number + Fast OTP", reply_markup=country_menu(0))

@bot.message_handler(commands=['pricelist'])
def price_h(m):
    txt="💰 PRICE LIST - Whatsapp Only 💰\n━━━━━━━━━━━━\n"
    for name,wp in list(WEBSITE_SERVERS.items())[:30]:
        flag,_=get_flag(name); txt+=f"{flag} {name} - ₹{wp+PROFIT}\n"
    txt+=f"\n...and more! Use /buy to see all 62+ servers"
    bot.send_message(m.chat.id, txt, reply_markup=main_kb())

@bot.message_handler(commands=['howtobuy'])
def how_h(m):
    txt=f"""❓ HOW TO BUY ❓
━━━━━━━━━━━━
1️⃣ /buy → Server select karo
2️⃣ UPI / USDT select karo
3️⃣ QR pe pay karo 💳
4️⃣ Screenshot bhejo 📸
5️⃣ Admin verify ✅
6️⃣ Number + OTP auto 🔑

💳 UPI: {UPI_ID}
🌍 USDT: {USDT_ADDRESS}
📞 @just_zevric"""
    bot.send_message(m.chat.id, txt, reply_markup=main_kb())

@bot.message_handler(commands=['support'])
def sup_h(m):
    mk=types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("📞 Contact @just_zevric", url=SUPPORT_LINK)); mk.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main"))
    bot.send_message(m.chat.id, f"📞 SUPPORT\n👤 @just_zevric\n🔗 {SUPPORT_LINK}\n⚡ 24/7 Fast Reply", reply_markup=mk)

@bot.message_handler(commands=['balance','admin'])
def bal_h(m):
    if m.from_user.id!=ADMIN_ID:
        bot.send_message(m.chat.id, "❌ Ye command sirf Admin ke liye hai!\nUse /buy to buy numbers.")
        return
    bot.send_message(m.chat.id, f"💰 PremiumOTP Balance: {api_bal()}\n💵 Profit: ₹{PROFIT}/number\n📊 Servers: {len(WEBSITE_SERVERS)}\n\n🔒 Ye message sirf aapko dikh raha hai (Admin only)")

@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    try:
        d=call.data
        if d=="main": start_h(call.message)
        elif d=="buy": bot.edit_message_text("📱 SELECT SERVER - Whatsapp Only ✅", call.message.chat.id, call.message.message_id, reply_markup=country_menu(0))
        elif d=="pricelist": price_h(call.message)
        elif d=="howtobuy": how_h(call.message)
        elif d.startswith("p_"): p=int(d.split("_")[1]); bot.edit_message_text(f"📱 Page {p+1}", call.message.chat.id, call.message.message_id, reply_markup=country_menu(p))
        elif d.startswith("c_"):
            server=d[2:]; bp=WEBSITE_SERVERS.get(server,50)+PROFIT; flag,code=get_flag(server); user_selection[call.from_user.id]=server
            txt=f"✅ {flag} {server}\n📱 Whatsapp Only\n🌍 {code}\n💰 Price: ₹{bp}\n\n💳 Select Payment:"
            mk=types.InlineKeyboardMarkup(row_width=2); mk.add(types.InlineKeyboardButton("🇮🇳 UPI 💳", callback_data=f"payupi_{server}"), types.InlineKeyboardButton("🌍 USDT 💵", callback_data=f"payusdt_{server}")); mk.add(types.InlineKeyboardButton("⬅️ Back", callback_data="buy"))
            bot.edit_message_text(txt, call.message.chat.id, call.message.message_id, reply_markup=mk)
        elif d.startswith("payupi_"):
            server=d.split("payupi_")[1]; bp=WEBSITE_SERVERS.get(server,50)+PROFIT; user_selection[call.from_user.id]=server; qr=make_upi_qr(bp)
            txt=f"🇮🇳 UPI - {server}\n💰 ₹{bp}\n💳 {UPI_ID}\n📸 Pay karke screenshot bhejo!"
            mk=types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"c_{server}"))
            if qr and os.path.exists(qr):
                with open(qr,'rb') as f: bot.send_photo(call.message.chat.id, f, caption=txt, reply_markup=mk)
            else: bot.send_message(call.message.chat.id, txt, reply_markup=mk)
        elif d.startswith("payusdt_"):
            server=d.split("payusdt_")[1]; bp=WEBSITE_SERVERS.get(server,50)+PROFIT; user_selection[call.from_user.id]=server; qr=make_usdt_qr()
            txt=f"🌍 USDT - {server}\n💰 ₹{bp}\n💳 {USDT_ADDRESS}"
            mk=types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"c_{server}"))
            if qr and os.path.exists(qr):
                with open(qr,'rb') as f: bot.send_photo(call.message.chat.id, f, caption=txt, reply_markup=mk)
            else: bot.send_message(call.message.chat.id, txt, reply_markup=mk)
        elif d.startswith("ap_"):
            parts=d.split("_",2); uid=int(parts[1]); server=parts[2] if len(parts)>2 else pending_orders.get(uid,{}).get("server","USA server 25")
            web=WEBSITE_SERVERS.get(server,50); bp=web+PROFIT; flag,_=get_flag(server)
            bot.answer_callback_query(call.id, "Buying...")
            bot.edit_message_text(f"✅ Approving {uid}... {flag} {server}\n💰 Cost ₹{web} Sell ₹{bp} Profit ₹{PROFIT} (Only you can see this)", call.message.chat.id, call.message.message_id)
            res=api_buy(server)
            if res and res.get("number"):
                phone=res["number"]; oid=res["id"]; user_numbers[uid]=phone; user_activations[uid]=oid
                txt=f"✅ PAYMENT VERIFIED! 🎉\n━━━━━━━━━━━━\n{flag} {server} ✅\n💰 ₹{bp}\n📱 Number: {phone}\n🆔 Order: {oid}\n━━━━━━━━━━━━\n📲 Whatsapp login:\n1️⃣ {phone}\n2️⃣ Get OTP dabao 👇\n🤖 Bot auto OTP dega!\n⏳ 15 min me OTP lo, warna number expire!"
                bot.send_message(uid, txt, reply_markup=after_number_kb(uid))
                bot.send_message(call.message.chat.id, f"✅ Delivered {uid}: {phone} | Profit ₹{PROFIT}")
            else:
                bot.send_message(uid, f"⚠️ API failed: {res.get('error')} Contact @just_zevric")
                bot.send_message(call.message.chat.id, f"❌ Failed {uid}: {res.get('error')}")
        elif d.startswith("rj_"):
            uid=int(d.split("_")[1]); bot.send_message(uid, "❌ Payment Rejected! Real screenshot bhejo!"); bot.edit_message_text(f"❌ Rejected {uid}", call.message.chat.id, call.message.message_id); bot.answer_callback_query(call.id, "Rejected")
        elif d.startswith("go_"):
            uid=int(d.split("_")[1]); oid=user_activations.get(uid)
            if not oid: bot.send_message(uid, "❌ Order not found! /start karo", reply_markup=main_kb()); return
            bot.answer_callback_query(call.id, "Checking...")
            otp=api_otp(oid)
            if otp:
                bot.send_message(uid, f"🔑 OTP READY! 🎉\n📱 {user_numbers.get(uid,'')}\n🔐 OTP: {otp}\n⚡ Jaldi daalo!", reply_markup=after_number_kb(uid))
            else:
                mk=types.InlineKeyboardMarkup(row_width=1)
                mk.add(types.InlineKeyboardButton("🔄 Try Again OTP", callback_data=f"go_{uid}"))
                mk.add(types.InlineKeyboardButton("🏠 Main Menu", callback_data="main"))
                mk.add(types.InlineKeyboardButton("❌ Cancel & Refund", callback_data=f"cancel_{oid}"))
                bot.send_message(uid, f"⏳ OTP abhi nahi aaya! Order {oid}\n📲 Pehle Whatsapp me OTP request karo, phir yahan Try Again dabao.\n⏰ 15 min ke andar OTP lo!", reply_markup=mk)
        elif d.startswith("cancel_"):
            oid=d.split("_")[1]
            if "ALREADY" in oid or not oid: bot.answer_callback_query(call.id, "Already canceled!"); return
            res=api_cancel(oid)
            if "ALREADY_CANCELED" in res: bot.answer_callback_query(call.id, "Already canceled!"); return
            bot.send_message(call.message.chat.id, f"✅ Canceled {oid}: {res}", reply_markup=main_kb())
            for u, o in list(user_activations.items()):
                if o==oid:
                    bot.send_message(u, f"✅ Order {oid} canceled! Refund ke liye @just_zevric se contact karo.", reply_markup=main_kb())
                    break
    except Exception as e: print(f"CB Error {e}")

@bot.message_handler(content_types=['photo'])
def photo_h(message):
    uid=message.from_user.id; server=user_selection.get(uid)
    if not server: bot.send_message(message.chat.id, "⚠️ Pehle /buy se server select karo!", reply_markup=main_kb()); return
    web=WEBSITE_SERVERS.get(server,50); bp=web+PROFIT; pending_orders[uid]={"server":server}
    flag,_=get_flag(server); uname=f"@{message.from_user.username}" if message.from_user.username else ""; name=message.from_user.first_name or ""
    # This message ONLY goes to admin, with profit details
    txt=f"🔒 NEW ORDER 🔒\n👤 {name} {uname} | {uid}\n🌍 {flag} {server}\n💰 Cost ₹{web} → Sell ₹{bp} = Profit ₹{PROFIT}\nServer: {server}\n\n⚠️ Check REAL payment! (Only Admin can see profit)"
    bot.send_message(ADMIN_ID, txt); bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    mk=types.InlineKeyboardMarkup(row_width=2); mk.add(types.InlineKeyboardButton(f"✅ Approve ₹{bp}", callback_data=f"ap_{uid}_{server}"), types.InlineKeyboardButton("❌ Reject", callback_data=f"rj_{uid}"))
    bot.send_message(ADMIN_ID, "Action:", reply_markup=mk)
    bot.send_message(message.chat.id, f"📸 Received! {flag} {server} - ₹{bp}\n🔒 Verifying 30 sec... ⏳", reply_markup=main_kb())

print(f"BOT FINAL - Admin Balance Hidden - Back Button Fixed - Profit Hidden")
app=Flask(__name__)
@app.route('/')
def home(): return f"Zevric - Admin Hidden - Profit {PROFIT}"
def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_web).start()
bot.infinity_polling(skip_pending=True, timeout=15)
