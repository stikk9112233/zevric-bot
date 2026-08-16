import telebot
from telebot import types
import os
import requests
from flask import Flask
import threading
import time

BOT_TOKEN = os.getenv("BOT_TOKEN", "8855823255:AAGe8a9FYnjIJTz2WWncDJ7kenDbLI4YMBE")
ADMIN_ID = 8981733976
UPI_ID = "zervicxplay@okhdfcbank"
USDT_ADDRESS = "TLwAWcJ7Tm34jqyYqV6qhizQHy8pe7US1V"
SUPPORT_USERNAME = "just_zevric"
SUPPORT_LINK = "https://t.me/just_zevric"

API_KEY = os.getenv("API_KEY", "ffcc751480b3c67244ea7123acbeb608")
API_BASE = "https://premiumotp.pro/api/v1/stark"

COUNTRIES = {
    "ARGENTINA_SERVER_1": {"flag": "🇦🇷", "sname": "Argentina server 1", "code": "+54", "price": 95, "country": "argentina", "server": "server1"},
    "BANGLADESH_SERVER_1": {"flag": "🇧🇩", "sname": "Bangladesh server 1", "code": "+880", "price": 95, "country": "bangladesh", "server": "server1"},
    "BANGLADESH_SERVER_3": {"flag": "🇧🇩", "sname": "Bangladesh server 3", "code": "+880", "price": 115, "country": "bangladesh", "server": "server2"},
    "BRAZIL": {"flag": "🇧🇷", "sname": "Brazil", "code": "+55", "price": 190, "country": "brazil", "server": "server1"},
    "CANADA_SERVER_14": {"flag": "🇨🇦", "sname": "Canada server 14", "code": "+1", "price": 82, "country": "canada", "server": "server1"},
    "CANADA_SERVER_15": {"flag": "🇨🇦", "sname": "Canada server 15", "code": "+1", "price": 82, "country": "canada", "server": "server1"},
    "CANADA_SERVER_16": {"flag": "🇨🇦", "sname": "Canada server 16", "code": "+1", "price": 90, "country": "canada", "server": "server1"},
    "CANADA_SERVER_18": {"flag": "🇨🇦", "sname": "Canada server 18", "code": "+1", "price": 139, "country": "canada", "server": "server1"},
    "CANADA_SERVER_21": {"flag": "🇨🇦", "sname": "Canada server 21", "code": "+1", "price": 95, "country": "canada", "server": "server1"},
    "CANADA_SERVER_22": {"flag": "🇨🇦", "sname": "Canada server 22", "code": "+1", "price": 93, "country": "canada", "server": "server1"},
    "CANADA_SERVER_3": {"flag": "🇨🇦", "sname": "Canada server 3", "code": "+1", "price": 92, "country": "canada", "server": "server1"},
    "CHILE": {"flag": "🇨🇱", "sname": "Chile", "code": "+56", "price": 75, "country": "chile", "server": "server1"},
    "CHILE_SERVER_1": {"flag": "🇨🇱", "sname": "Chile server 1", "code": "+56", "price": 68, "country": "chile", "server": "server1"},
    "CHILE_SERVER_2": {"flag": "🇨🇱", "sname": "Chile server 2", "code": "+56", "price": 80, "country": "chile", "server": "server1"},
    "COLOMBIA": {"flag": "🇨🇴", "sname": "Colombia", "code": "+57", "price": 75, "country": "colombia", "server": "server1"},
    "COLOMBIA_SERVER_1": {"flag": "🇨🇴", "sname": "Colombia server 1", "code": "+57", "price": 95, "country": "colombia", "server": "server1"},
    "COLOMBIA_SERVER_5": {"flag": "🇨🇴", "sname": "Colombia server 5", "code": "+57", "price": 95, "country": "colombia", "server": "server1"},
    "COLOMBIA_SERVER_8": {"flag": "🇨🇴", "sname": "Colombia server 8", "code": "+57", "price": 82, "country": "colombia", "server": "server1"},
    "INDIA_SERVER_10": {"flag": "🇮🇳", "sname": "India server 10", "code": "+91", "price": 152, "country": "india", "server": "server1"},
    "INDIA_SERVER_25": {"flag": "🇮🇳", "sname": "India server 25", "code": "+91", "price": 160, "country": "india", "server": "server1"},
    "INDONESIA": {"flag": "🇮🇩", "sname": "Indonesia", "code": "+62", "price": 68, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_12": {"flag": "🇮🇩", "sname": "Indonesia server 12", "code": "+62", "price": 65, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_14": {"flag": "🇮🇩", "sname": "Indonesia server 14", "code": "+62", "price": 65, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_15": {"flag": "🇮🇩", "sname": "Indonesia server 15", "code": "+62", "price": 63, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_16": {"flag": "🇮🇩", "sname": "Indonesia server 16", "code": "+62", "price": 65, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_17": {"flag": "🇮🇩", "sname": "Indonesia server 17", "code": "+62", "price": 65, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_18": {"flag": "🇮🇩", "sname": "Indonesia server 18", "code": "+62", "price": 65, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_2": {"flag": "🇮🇩", "sname": "Indonesia server 2", "code": "+62", "price": 65, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_6": {"flag": "🇮🇩", "sname": "Indonesia server 6", "code": "+62", "price": 73, "country": "indonesia", "server": "server1"},
    "INDONESIA_SERVER_9": {"flag": "🇮🇩", "sname": "Indonesia server 9", "code": "+62", "price": 64, "country": "indonesia", "server": "server1"},
    "IVORY_COAST": {"flag": "🇨🇮", "sname": "Ivory Coast", "code": "+225", "price": 65, "country": "ivorycoast", "server": "server1"},
    "KENYA_SERVER_1": {"flag": "🇰🇪", "sname": "Kenya server 1", "code": "+254", "price": 80, "country": "kenya", "server": "server1"},
    "MALAYSIA_SERVER_1": {"flag": "🇲🇾", "sname": "Malaysia server 1", "code": "+60", "price": 125, "country": "malaysia", "server": "server1"},
    "MALAYSIA_SERVER_2": {"flag": "🇲🇾", "sname": "Malaysia server 2", "code": "+60", "price": 129, "country": "malaysia", "server": "server1"},
    "MAURITANIA_SERVER_1": {"flag": "🇲🇷", "sname": "Mauritania server 1", "code": "+222", "price": 80, "country": "mauritania", "server": "server1"},
    "NEPAL_SERVER_2": {"flag": "🇳🇵", "sname": "Nepal server 2", "code": "+977", "price": 95, "country": "nepal", "server": "server1"},
    "NETHERLANDS": {"flag": "🇳🇱", "sname": "Netherlands", "code": "+31", "price": 195, "country": "netherlands", "server": "server1"},
    "PHILIPPINES": {"flag": "🇵🇭", "sname": "Philippines", "code": "+63", "price": 67, "country": "philippines", "server": "server1"},
    "PHILIPPINES_SERVER_3": {"flag": "🇵🇭", "sname": "Philippines server 3", "code": "+63", "price": 85, "country": "philippines", "server": "server1"},
    "PHILIPPINES_SERVER_5": {"flag": "🇵🇭", "sname": "Philippines server 5", "code": "+63", "price": 90, "country": "philippines", "server": "server1"},
    "POLAND_SERVER_1": {"flag": "🇵🇱", "sname": "Poland server 1", "code": "+48", "price": 130, "country": "poland", "server": "server1"},
    "SAUDI_ARABIA_SERVER_1": {"flag": "🇸🇦", "sname": "Saudi Arabia server 1", "code": "+966", "price": 100, "country": "saudiarabia", "server": "server1"},
    "SOUTH_AFRICA": {"flag": "🇿🇦", "sname": "South Africa", "code": "+27", "price": 65, "country": "southafrica", "server": "server1"},
    "SOUTH_AFRICA_SERVER_3": {"flag": "🇿🇦", "sname": "South Africa server 3", "code": "+27", "price": 63, "country": "southafrica", "server": "server1"},
    "SOUTH_AFRICA_SERVER_6": {"flag": "🇿🇦", "sname": "South Africa server 6", "code": "+27", "price": 62, "country": "southafrica", "server": "server1"},
    "SOUTH_AFRICA_SERVER_7": {"flag": "🇿🇦", "sname": "South Africa server 7", "code": "+27", "price": 59, "country": "southafrica", "server": "server1"},
    "SOUTH_AFRICA_SERVER_8": {"flag": "🇿🇦", "sname": "South Africa server 8", "code": "+27", "price": 60, "country": "southafrica", "server": "server1"},
    "THAILAND_SERVER_1": {"flag": "🇹🇭", "sname": "Thailand server 1", "code": "+66", "price": 100, "country": "thailand", "server": "server1"},
    "THAILAND_SERVER_3": {"flag": "🇹🇭", "sname": "Thailand server 3", "code": "+66", "price": 113, "country": "thailand", "server": "server1"},
    "USA": {"flag": "🇺🇸", "sname": "USA", "code": "+1", "price": 155, "country": "usa", "server": "server1"},
    "USA_SERVER_0": {"flag": "🇺🇸", "sname": "USA server 0", "code": "+1", "price": 110, "country": "usa", "server": "server1"},
    "USA_SERVER_1": {"flag": "🇺🇸", "sname": "USA server 1", "code": "+1", "price": 239, "country": "usa", "server": "server1"},
    "USA_SERVER_12": {"flag": "🇺🇸", "sname": "USA server 12", "code": "+1", "price": 68, "country": "usa", "server": "server1"},
    "USA_SERVER_17": {"flag": "🇺🇸", "sname": "USA server 17", "code": "+1", "price": 65, "country": "usa", "server": "server1"},
    "USA_SERVER_25": {"flag": "🇺🇸", "sname": "USA server 25", "code": "+1", "price": 100, "country": "usa", "server": "server1"},
    "USA_SERVER_26": {"flag": "🇺🇸", "sname": "USA server 26", "code": "+1", "price": 80, "country": "usa", "server": "server1"},
    "UNITED_KINGDOM": {"flag": "🇬🇧", "sname": "United Kingdom", "code": "+44", "price": 105, "country": "england", "server": "server1"},
    "UNITED_KINGDOM_SERVER_2": {"flag": "🇬🇧", "sname": "UK server 2", "code": "+44", "price": 145, "country": "england", "server": "server1"},
    "UZBEKISTAN_SERVER_1": {"flag": "🇺🇿", "sname": "Uzbekistan server 1", "code": "+998", "price": 130, "country": "uzbekistan", "server": "server1"},
    "VIETNAM_SERVER_1": {"flag": "🇻🇳", "sname": "Vietnam server 1", "code": "+84", "price": 90, "country": "vietnam", "server": "server1"},
    "VIETNAM_SERVER_2": {"flag": "🇻🇳", "sname": "Vietnam server 2", "code": "+84", "price": 75, "country": "vietnam", "server": "server1"},
    "YEMEN_SERVER_1": {"flag": "🇾🇪", "sname": "Yemen server 1", "code": "+967", "price": 62, "country": "yemen", "server": "server1"},
}

bot = telebot.TeleBot(BOT_TOKEN)
bot.delete_webhook()
try:
    import qrcode
    QR_OK = True
except:
    QR_OK = False

user_selection = {}
user_numbers = {}
user_activations = {}
pending_orders = {}  # uid -> {server_key, info}

def set_commands():
    try:
        bot.delete_my_commands()
        bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    except: pass
    try:
        cmds = [types.BotCommand("start", "🔥 ZEVRIC OTP BAZAAR"), types.BotCommand("buy", "🛒 Buy Whatsapp Number"), types.BotCommand("balance", "💰 Check API Balance")]
        bot.set_my_commands(cmds)
    except: pass
set_commands()

def api_get_balance():
    try:
        url = f"{API_BASE}?api_key={API_KEY}&action=getBalance"
        r = requests.get(url, timeout=10)
        return r.text
    except Exception as e:
        return f"Error: {e}"

def api_buy_number(server_param="server1"):
    try:
        url = f"{API_BASE}?api_key={API_KEY}&action=getNumber&service=wa&server={server_param}"
        print(f"Buying: {url}")
        r = requests.get(url, timeout=15)
        print(f"Buy Response: {r.text}")
        txt = r.text.strip()
        if "ACCESS_NUMBER" in txt:
            parts = txt.split(":")
            order_id = parts[1]
            phone = parts[2]
            return {"id": order_id, "number": phone, "raw": txt}
        else:
            return {"error": txt}
    except Exception as e:
        return {"error": str(e)}

def api_get_otp(order_id):
    try:
        url = f"{API_BASE}?api_key={API_KEY}&action=getStatus&id={order_id}"
        r = requests.get(url, timeout=10)
        txt = r.text.strip()
        if "STATUS_OK" in txt:
            code = txt.split(":")[1]
            return code
        else:
            return None
    except:
        return None

def api_cancel(order_id):
    try:
        url = f"{API_BASE}?api_key={API_KEY}&action=setStatus&id={order_id}&status=8"
        r = requests.get(url, timeout=10)
        return r.text
    except: return None

def make_upi_qr(amount):
    if not QR_OK: return None
    try:
        import qrcode
        upi_str = f"upi://pay?pa={UPI_ID}&pn=ZEVRIC OTP BAZAAR&am={amount}&cu=INR"
        qr = qrcode.make(upi_str)
        path = f"/tmp/qr_upi_{amount}.png"
        qr.save(path)
        return path
    except: return None

def make_usdt_qr():
    if not QR_OK: return None
    try:
        import qrcode
        qr = qrcode.make(USDT_ADDRESS)
        path = f"/tmp/qr_usdt.png"
        qr.save(path)
        return path
    except: return None

def country_menu(page=0):
    items = list(COUNTRIES.items())
    per_page = 8
    s = page*per_page
    e = s+per_page
    mk = types.InlineKeyboardMarkup(row_width=1)
    for k, d in items[s:e]:
        mk.add(types.InlineKeyboardButton(f"{d['flag']} {d['sname']} {d['code']} - ₹{d['price']} ✅", callback_data=f"c_{k}"))
    nav = []
    if page>0: nav.append(types.InlineKeyboardButton("⬅️ Prev", callback_data=f"p_{page-1}"))
    if e < len(items): nav.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"p_{page+1}"))
    if nav: mk.row(*nav)
    mk.add(types.InlineKeyboardButton("🔙 Main Menu 🏠", callback_data="main"))
    return mk

def payment_method_menu(server_key):
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(types.InlineKeyboardButton("🇮🇳 BUY with UPI", callback_data=f"payupi_{server_key}"), types.InlineKeyboardButton("🌍 BUY with USDT", callback_data=f"payusdt_{server_key}"))
    mk.add(types.InlineKeyboardButton("⬅️ Back to Servers", callback_data="buy"))
    return mk

@bot.message_handler(commands=['start'])
def start_handler(message):
    txt = f"""🔥 <b>ZEVRIC OTP BAZAAR - SECURE MODE 🔒</b> 🔥
━━━━━━━━━━━━━━━━━━━━
💜 <b>Only WhatsApp - Admin Verified!</b> 💜
━━━━━━━━━━━━━━━━━━━━
🚀 62 Servers - Whatsapp Only ✅
🔒 Fake Payment Protection ON
⚡ API: premiumotp.pro Connected

No Auto loss - Admin check ke baad number milega!
━━━━━━━━━━━━━━━━━━━━"""
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("🛒 Buy Whatsapp Number 🔥", callback_data="buy"), types.InlineKeyboardButton("💰 Balance", callback_data="bal"))
    m.add(types.InlineKeyboardButton("📞 Support", url=SUPPORT_LINK))
    bot.send_message(message.chat.id, txt, parse_mode="HTML", reply_markup=m)

@bot.message_handler(commands=['buy'])
def buy_handler(message):
    bot.send_message(message.chat.id, "📱 <b>SELECT SERVER - ONLY WHATSAPP ✅</b>\n🔒 Secure Mode - Admin will verify payment!", parse_mode="HTML", reply_markup=country_menu(0))

@bot.message_handler(commands=['balance'])
def balance_handler(message):
    if message.from_user.id != ADMIN_ID: return
    bal = api_get_balance()
    bot.send_message(message.chat.id, f"💰 Balance: <code>{bal}</code>", parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    try:
        d = call.data
        if d == "main":
            start_handler(call.message)
        elif d == "buy":
            bot.edit_message_text("📱 <b>SELECT SERVER - Whatsapp Only ✅</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=country_menu(0))
        elif d == "bal":
            bal = api_get_balance()
            bot.answer_callback_query(call.id, f"Balance: {bal}")
            bot.send_message(call.message.chat.id, f"💰 Balance: <code>{bal}</code>", parse_mode="HTML")
        elif d.startswith("p_"):
            page = int(d.split("_")[1])
            bot.edit_message_text(f"📱 Page {page+1}", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=country_menu(page))
        elif d.startswith("c_"):
            key = d[2:]
            info = COUNTRIES.get(key)
            if not info: return
            user_selection[call.from_user.id] = key
            caption = f"✅ <b>{info['flag']} {info['sname']}</b>\n📱 Whatsapp Only (wa)\n🌍 {info['country']} {info['code']}\n💰 ₹{info['price']} / ${round(info['price']/85,2)}\n💳 Payment Chunno:"
            bot.edit_message_text(caption, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=payment_method_menu(key))
        elif d.startswith("payupi_"):
            key = d.split("payupi_")[1]
            info = COUNTRIES.get(key)
            user_selection[call.from_user.id] = key
            qr_path = make_upi_qr(info['price'])
            caption = f"🇮🇳 <b>UPI - {info['flag']} {info['sname']} (Whatsapp)</b>\n💰 ₹{info['price']}\nUPI: <code>{UPI_ID}</code>\nPay and send screenshot - Admin verify karega! 🔒"
            mk = types.InlineKeyboardMarkup()
            mk.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"c_{key}"))
            if qr_path and os.path.exists(qr_path):
                with open(qr_path,'rb') as f: bot.send_photo(call.message.chat.id, f, caption=caption, parse_mode="HTML", reply_markup=mk)
            else: bot.send_message(call.message.chat.id, caption, parse_mode="HTML", reply_markup=mk)
        elif d.startswith("payusdt_"):
            key = d.split("payusdt_")[1]
            info = COUNTRIES.get(key)
            user_selection[call.from_user.id] = key
            qr_path = make_usdt_qr()
            caption = f"🌍 <b>USDT - {info['flag']} {info['sname']} (Whatsapp)</b>\n💰 ${round(info['price']/85,2)}\n<code>{USDT_ADDRESS}</code>\nPay and send TxID - Admin verify karega! 🔒"
            mk = types.InlineKeyboardMarkup()
            mk.add(types.InlineKeyboardButton("⬅️ Back", callback_data=f"c_{key}"))
            if qr_path and os.path.exists(qr_path):
                with open(qr_path,'rb') as f: bot.send_photo(call.message.chat.id, f, caption=caption, parse_mode="HTML", reply_markup=mk)
            else: bot.send_message(call.message.chat.id, caption, parse_mode="HTML", reply_markup=mk)
        elif d.startswith("ap_"):
            # ADMIN APPROVE - NOW BUY FROM API
            try:
                uid = int(d.split("_")[1])
                server_key = d.split("_", 2)[2] if len(d.split("_"))>2 else pending_orders.get(uid, {}).get("key", "server1")
                info = COUNTRIES.get(server_key) or pending_orders.get(uid, {}).get("info") or {"flag":"🇺🇸","sname":"USA","server":"server1","price":95}
                
                bot.answer_callback_query(call.id, "Approving & Buying from API...")
                bot.edit_message_text(f"✅ Approving {uid}... Buying from premiumotp.pro API... ⏳", call.message.chat.id, call.message.message_id)
                
                result = api_buy_number(info.get("server","server1"))
                if result and result.get("number"):
                    phone = result["number"]
                    order_id = result["id"]
                    user_numbers[uid] = phone
                    user_activations[uid] = order_id
                    
                    mk = types.InlineKeyboardMarkup()
                    mk.add(types.InlineKeyboardButton("🔑 Get OTP (Auto) - Click Here 👇", callback_data=f"go_{uid}"))
                    mk.add(types.InlineKeyboardButton("❌ Cancel & Refund", callback_data=f"cancel_{order_id}"))
                    
                    txt = f"✅ <b>PAYMENT VERIFIED + WHATSAPP NUMBER! 🎉</b>\n━━━━━━━━━━━━\n{info['flag']} {info['sname']} - Whatsapp Only ✅\n💰 ₹{info['price']}\n📱 Number: <code>{phone}</code>\n🆔 Order: <code>{order_id}</code>\n━━━━━━━━━━━━\n📲 <b>Whatsapp me login karo:</b>\n1️⃣ Number: <code>{phone}</code>\n2️⃣ Get OTP dabao 👇\n🤖 Bot auto OTP dega!"
                    bot.send_message(uid, txt, parse_mode="HTML", reply_markup=mk)
                    bot.send_message(call.message.chat.id, f"✅ Auto Delivered to {uid}: {phone} | Order {order_id} | {info['flag']} ₹{info['price']}")
                else:
                    err = result.get("error","Unknown") if result else "No response"
                    bot.send_message(uid, f"⚠️ Admin ne approve kiya but API me number nahi mila!\nError: {err}\n@just_zevric ko bolo, refund/ dusra number milega!")
                    bot.send_message(call.message.chat.id, f"❌ API Buy Failed for {uid}: {err}")
            except Exception as e:
                bot.send_message(call.message.chat.id, f"Approve Error: {e}")
        elif d.startswith("rj_"):
            uid = int(d.split("_")[1])
            bot.send_message(uid, "❌ <b>Payment Rejected!</b>\nAdmin ne fake payment detect kiya! Real screenshot bhejo!", parse_mode="HTML")
            bot.answer_callback_query(call.id, "Rejected - User informed")
            bot.edit_message_text(f"❌ Rejected {uid} - Fake payment", call.message.chat.id, call.message.message_id)
        elif d.startswith("go_"):
            uid = int(d.split("_")[1])
            order_id = user_activations.get(uid)
            if not order_id:
                bot.send_message(uid, "❌ Order ID nahi mila! @just_zevric ko bolo", parse_mode="HTML")
                return
            bot.send_message(uid, f"🔍 <b>Checking OTP... Order {order_id}</b>\n10 sec wait...", parse_mode="HTML")
            otp = None
            for i in range(12):
                otp = api_get_otp(order_id)
                if otp:
                    break
                time.sleep(10)
            if otp:
                num = user_numbers.get(uid, "")
                bot.send_message(uid, f"🔑 <b>OTP READY! 🎉</b>\n📱 {num}\n🔐 OTP: <code>{otp}</code>\n⚡ Jaldi daalo!", parse_mode="HTML")
                bot.send_message(ADMIN_ID, f"✅ OTP delivered to {uid}: {otp} | {num}")
            else:
                bot.send_message(uid, f"⏳ OTP abhi nahi aaya! Order: {order_id}\n1 min baad fir dabao!", parse_mode="HTML")
            bot.answer_callback_query(call.id, "Checked!")
        elif d.startswith("cancel_"):
            order_id = d.split("_")[1]
            res = api_cancel(order_id)
            bot.send_message(call.message.chat.id, f"Cancel {order_id}: {res}")
    except Exception as e:
        print(f"CB Error: {e}")

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    uid = message.from_user.id
    sel = user_selection.get(uid)
    if not sel:
        bot.send_message(message.chat.id, "⚠️ Pehle /buy se server select karo! 📱", parse_mode="HTML")
        return
    info = COUNTRIES[sel]
    pending_orders[uid] = {"key": sel, "info": info}
    
    # SECURE MODE - NO AUTO BUY, SEND TO ADMIN FOR VERIFICATION
    username = f"@{message.from_user.username}" if message.from_user.username else "No username"
    name = message.from_user.first_name or ""
    
    txt_admin = f"🔒 <b>NEW ORDER - VERIFY PAYMENT! 🔒</b>\n━━━━━━━━━━━━\n👤 {name} {username}\n🆔 {uid}\n🌍 {info['flag']} {info['sname']}\n💰 ₹{info['price']}\n📱 Whatsapp Only (wa)\nServer Param: {info['server']}\n━━━━━━━━━━━━\n⚠️ <b>Check payment REAL hai ya FAKE?</b>\nAgar real hai to ✅ Approve dabao - tabhi API se number ayega!\nFake hai to ❌ Reject!"
    bot.send_message(ADMIN_ID, txt_admin, parse_mode="HTML")
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    
    mk = types.InlineKeyboardMarkup(row_width=2)
    mk.add(types.InlineKeyboardButton(f"✅ Approve & Auto Buy {info['flag']}", callback_data=f"ap_{uid}_{sel}"), types.InlineKeyboardButton("❌ Reject Fake", callback_data=f"rj_{uid}"))
    bot.send_message(ADMIN_ID, "👇 Verify & Action Lo:", reply_markup=mk)
    
    bot.send_message(message.chat.id, f"📸 Screenshot Received! ✅\n{info['flag']} {info['sname']} - ₹{info['price']}\n🔒 Admin payment verify kar raha hai (30 sec)...\nReal payment hua toh auto number milega! ⚡", parse_mode="HTML")

print("SECURE BOT - MANUAL VERIFY + AUTO API DELIVERY - STARTED 🔒🤖")
app = Flask(__name__)
@app.route('/')
def home():
    return "Zevric Secure Bot - Whatsapp Only - Manual Verify + Auto API"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_web).start()
bot.infinity_polling(skip_pending=True, timeout=10, long_polling_timeout=10, allowed_updates=["message","callback_query"], none_stop=True)
