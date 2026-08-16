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
PROFIT = 40  # Sirf admin ko pata chalega, customer ko nahi!

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
    "Argentina": "ð¦ð· +54", "Bangladesh": "ð§ð© +880", "Brazil": "ð§ð· +55", "Canada": "ð¨ð¦ +1",
    "Chile": "ð¨ð± +56", "Colombia": "ð¨ð´ +57", "India": "ð®ð³ +91", "Indonesia": "ð®ð© +62",
    "Ivory Coast": "ð¨ð® +225", "Kenya": "ð°ðª +254", "Malaysia": "ð²ð¾ +60", "Mauritania": "ð²ð· +222",
    "Nepal": "ð³ðµ +977", "Netherlands": "ð³ð± +31", "Philippines": "ðµð­ +63", "Poland": "ðµð± +48",
    "Saudi Arabia": "ð¸ð¦ +966", "South Africa": "ð¿ð¦ +27", "Thailand": "ð¹ð­ +66", "USA": "ðºð¸ +1",
    "United Kingdom": "ð¬ð§ +44", "Uzbekistan": "ðºð¿ +998", "Vietnam": "ð»ð³ +84", "Yemen": "ð¾ðª +967",
}
def get_flag_code(s):
    for c, fc in FLAGS.items():
        if c.lower() in s.lower():
            p = fc.split(" "); return p[0], " ".join(p[1:])
    return "ð", "+?"

bot = telebot.TeleBot(BOT_TOKEN)
bot.delete_webhook()
try: import qrcode; QR_OK=True
except: QR_OK=False

user_selection = {}; user_numbers = {}; user_activations = {}; pending_orders = {}

def set_commands():
    try:
        bot.delete_my_commands()
        bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    except: pass
    try:
        cmds = [
            types.BotCommand("start", "ð¥ Main Menu"),
            types.BotCommand("buy", "ð Buy Whatsapp Number"),
            types.BotCommand("pricelist", "ð° Price List"),
            types.BotCommand("howtobuy", "â How to Buy"),
            types.BotCommand("support", "ð Support"),
            types.BotCommand("balance", "ð° Admin Balance (Admin Only)"),
        ]
        bot.set_my_commands(cmds)
    except: pass
set_commands()

def api_get_balance():
    try: return requests.get(f"{API_BASE}?api_key={API_KEY}&action=getBalance", timeout=10).text
    except Exception as e: return str(e)

def api_buy_number_exact_server(server_exact_name):
    try:
        url = f"{API_BASE}?api_key={API_KEY}&action=getNumber&service=wa&server={server_exact_name}"
        print(f"Buying: {url}")
        r = requests.get(url, timeout=15); txt = r.text.strip()
        print(f"Response: {txt}")
        if "ACCESS_NUMBER" in txt: p=txt.split(":"); return {"id":p[1],"number":p[2],"raw":txt}
        if "NO_NUMBERS" in txt or "ERROR" in txt or "NO_BALANCE" in txt:
            # Fallback any server
            url2 = f"{API_BASE}?api_key={API_KEY}&action=getNumber&service=wa"
            r2 = requests.get(url2, timeout=15); txt2=r2.text.strip()
            print(f"Fallback: {txt2}")
            if "ACCESS_NUMBER" in txt2: p=txt2.split(":"); return {"id":p[1],"number":p[2],"raw":txt2}
        return {"error":txt}
    except Exception as e: return {"error":str(e)}

def api_get_otp(order_id):
    try:
        url = f"{API_BASE}?api_key={API_KEY}&action=getStatus&id={order_id}"
        r = requests.get(url, timeout=10); txt=r.text.strip()
        if "STATUS_OK" in txt: return txt.split(":")[1]
        return None
    except: return None

def api_cancel(order_id):
    try: return requests.get(f"{API_BASE}?api_key={API_KEY}&action=setStatus&id={order_id}&status=8", timeout=10).text
    except: return None

def make_upi_qr(amount):
    if not QR_OK: return None
    try:
        import qrcode; upi_str = f"upi://pay?pa={UPI_ID}&pn=ZEVRIC&am={amount}&cu=INR"
        qr = qrcode.make(upi_str); path = f"/tmp/qr_upi_{amount}.png"; qr.save(path); return path
    except: return None

def make_usdt_qr():
    if not QR_OK: return None
    try: import qrcode; qr=qrcode.make(USDT_ADDRESS); path="/tmp/qr_usdt.png"; qr.save(path); return path
    except: return None

def country_menu(page=0):
    items = list(WEBSITE_SERVERS.items()); per_page=8; s=page*per_page; e=s+per_page
    mk = types.InlineKeyboardMarkup(row_width=1)
    for server_name, web_price in items[s:e]:
        flag, code = get_flag_code(server_name); bot_price = web_price + PROFIT
        # Customer ko sirf bot price dikhega, cost+profit nahi dikhega
        mk.add(types.InlineKeyboardButton(f"{flag} {server_name} {code} - â¹{bot_price} â", callback_data=f"c_{server_name}"))
    nav=[]
    if page>0: nav.append(types.InlineKeyboardButton("â¬ï¸ Prev", callback_data=f"p_{page-1}"))
    if e < len(items): nav.append(types.InlineKeyboardButton("Next â¡ï¸", callback_data=f"p_{page+1}"))
    if nav: mk.row(*nav)
    mk.add(types.InlineKeyboardButton("ð Main Menu ð ", callback_data="main"))
    return mk

def main_menu_markup():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("ð Buy Whatsapp Number ð¥", callback_data="buy"), types.InlineKeyboardButton("ð° Price List", callback_data="pricelist"))
    m.add(types.InlineKeyboardButton("â How to Buy", callback_data="howtobuy"), types.InlineKeyboardButton("ð Support", url=SUPPORT_LINK))
    return m

@bot.message_handler(commands=['start'])
def start_handler(message):
    txt = """ð¥ <b>ZEVRIC OTP BAZAAR</b> ð¥
ââââââââââââââââââââ
ð <b>Only Whatsapp - Instant Delivery</b> ð
ââââââââââââââââââââ
ð 62+ Servers Available
â¡ Fast OTP - Auto Delivery
â Real Numbers - No Fake
ð 24/7 Support

ð Menu se select karo:"""
    bot.send_message(message.chat.id, txt, parse_mode="HTML", reply_markup=main_menu_markup())

@bot.message_handler(commands=['buy'])
def buy_handler(message):
    bot.send_message(message.chat.id, "ð± <b>SELECT SERVER - Whatsapp Only â</b>\nâ¡ Instant Number + Fast OTP", parse_mode="HTML", reply_markup=country_menu(0))

@bot.message_handler(commands=['pricelist'])
def pricelist_handler(message):
    txt = "ð° <b>PRICE LIST - Whatsapp Only</b>\nââââââââââââ\n"
    for server_name, web_price in list(WEBSITE_SERVERS.items())[:20]:
        flag, code = get_flag_code(server_name)
        bot_price = web_price + PROFIT
        txt += f"{flag} {server_name} - â¹{bot_price}\n"
    txt += f"\n...and {len(WEBSITE_SERVERS)-20} more servers!\nUse /buy to see all!"
    bot.send_message(message.chat.id, txt, parse_mode="HTML", reply_markup=main_menu_markup())

@bot.message_handler(commands=['howtobuy'])
def howtobuy_handler(message):
    txt = f"""â <b>HOW TO BUY - Step by Step</b>
ââââââââââââââââââââ
1ï¸â£ /buy dabao - Server select karo
2ï¸â£ UPI / USDT select karo
3ï¸â£ QR pe payment karo
4ï¸â£ Screenshot bhejo
5ï¸â£ Admin verify karega (30 sec)
6ï¸â£ Number + OTP auto milega!

ð³ <b>UPI:</b> <code>{UPI_ID}</code>
ð <b>USDT:</b> <code>{USDT_ADDRESS}</code>

ð Help: @just_zevric"""
    bot.send_message(message.chat.id, txt, parse_mode="HTML", reply_markup=main_menu_markup())

@bot.message_handler(commands=['support'])
def support_handler(message):
    txt = f"""ð <b>SUPPORT - ZEVRIC OTP BAZAAR</b>
ââââââââââââââââââââ
ð¤ Owner: @just_zevric
ð Link: {SUPPORT_LINK}
â¡ Fast Reply - 24/7

â Koi bhi problem ho toh direct message karo!"""
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("ð Contact Support", url=SUPPORT_LINK))
    m.add(types.InlineKeyboardButton("ð Main Menu", callback_data="main"))
    bot.send_message(message.chat.id, txt, parse_mode="HTML", reply_markup=m)

@bot.message_handler(commands=['balance'])
def balance_handler(message):
    if message.from_user.id != ADMIN_ID:
        bot.send_message(message.chat.id, "â Admin only command!")
        return
    bal = api_get_balance()
    bot.send_message(message.chat.id, f"ð° <b>PremiumOTP Balance:</b> <code>{bal}</code>\n\nðµ Profit per number: â¹{PROFIT}\nð Total servers: {len(WEBSITE_SERVERS)}\nð Website: premiumotp.pro\n\nâ ï¸ Customer ko profit nahi dikhta, sirf tujhe dikhta hai!", parse_mode="HTML")

@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    try:
        d=call.data
        if d=="main": start_handler(call.message)
        elif d=="buy":
            bot.edit_message_text("ð± <b>SELECT SERVER - Whatsapp Only â</b>", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=country_menu(0))
        elif d=="pricelist": pricelist_handler(call.message)
        elif d=="howtobuy": howtobuy_handler(call.message)
        elif d.startswith("p_"):
            page=int(d.split("_")[1])
            bot.edit_message_text(f"ð± Page {page+1} - Whatsapp Only", call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=country_menu(page))
        elif d.startswith("c_"):
            server_name=d[2:]; web_price=WEBSITE_SERVERS.get(server_name,50); bot_price=web_price+PROFIT; flag,code=get_flag_code(server_name)
            user_selection[call.from_user.id]=server_name
            # Customer ko sirf bot_price dikhega
            caption=f"â <b>{flag} {server_name}</b>\nð± Whatsapp Only (wa)\nð {code}\nð° Price: â¹{bot_price}\n\nð³ Payment Method Chunno:"
            mk=types.InlineKeyboardMarkup(row_width=2)
            mk.add(types.InlineKeyboardButton("ð®ð³ BUY with UPI", callback_data=f"payupi_{server_name}"), types.InlineKeyboardButton("ð BUY with USDT", callback_data=f"payusdt_{server_name}"))
            mk.add(types.InlineKeyboardButton("â¬ï¸ Back to Servers", callback_data="buy"))
            bot.edit_message_text(caption, call.message.chat.id, call.message.message_id, parse_mode="HTML", reply_markup=mk)
        elif d.startswith("payupi_"):
            server_name=d.split("payupi_")[1]; bot_price=WEBSITE_SERVERS.get(server_name,50)+PROFIT; user_selection[call.from_user.id]=server_name
            qr_path=make_upi_qr(bot_price)
            caption=f"ð®ð³ <b>UPI - {server_name}</b>\nð° Price: â¹{bot_price}\nUPI: <code>{UPI_ID}</code>\nPay and send screenshot! â"
            mk=types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("â¬ï¸ Back", callback_data=f"c_{server_name}"))
            if qr_path and os.path.exists(qr_path):
                with open(qr_path,'rb') as f: bot.send_photo(call.message.chat.id, f, caption=caption, parse_mode="HTML", reply_markup=mk)
            else: bot.send_message(call.message.chat.id, caption, parse_mode="HTML", reply_markup=mk)
        elif d.startswith("payusdt_"):
            server_name=d.split("payusdt_")[1]; bot_price=WEBSITE_SERVERS.get(server_name,50)+PROFIT; user_selection[call.from_user.id]=server_name
            qr_path=make_usdt_qr()
            caption=f"ð <b>USDT - {server_name}</b>\nð° â¹{bot_price} (${round(bot_price/85,2)})\n<code>{USDT_ADDRESS}</code>\nPay and send TxID! â"
            mk=types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("â¬ï¸ Back", callback_data=f"c_{server_name}"))
            if qr_path and os.path.exists(qr_path):
                with open(qr_path,'rb') as f: bot.send_photo(call.message.chat.id, f, caption=caption, parse_mode="HTML", reply_markup=mk)
            else: bot.send_message(call.message.chat.id, caption, parse_mode="HTML", reply_markup=mk)
        elif d.startswith("ap_"):
            try:
                parts=d.split("_",2); uid=int(parts[1]); server_name=parts[2] if len(parts)>2 else pending_orders.get(uid,{}).get("server","USA server 25")
                web_price=WEBSITE_SERVERS.get(server_name,50); bot_price=web_price+PROFIT; flag,code=get_flag_code(server_name)
                bot.answer_callback_query(call.id, "Buying from API...")
                bot.edit_message_text(f"â Approving {uid}...\n{flag} {server_name}\nCost â¹{web_price} Sell â¹{bot_price} Profit â¹{PROFIT} - Buying...", call.message.chat.id, call.message.message_id)
                result=api_buy_number_exact_server(server_name)
                if result and result.get("number"):
                    phone=result["number"]; order_id=result["id"]
                    user_numbers[uid]=phone; user_activations[uid]=order_id
                    mk=types.InlineKeyboardMarkup(); mk.add(types.InlineKeyboardButton("ð Get OTP (Auto) - Click Here ð", callback_data=f"go_{uid}")); mk.add(types.InlineKeyboardButton("â Cancel & Refund", callback_data=f"cancel_{order_id}"))
                    txt=f"â <b>PAYMENT APPROVED + WHATSAPP NUMBER AUTO! ð</b>\nââââââââââââ\n{flag} {server_name} - Whatsapp Only â\nð° â¹{bot_price}\nð± Number: <code>{phone}</code>\nð Order: <code>{order_id}</code>\nââââââââââââ\nð² <b>Whatsapp me login karo:</b>\n1ï¸â£ Number: <code>{phone}</code>\n2ï¸â£ Get OTP dabao ð\nð¤ Bot khud OTP dega!"
                    bot.send_message(uid, txt, parse_mode="HTML", reply_markup=mk)
                    bot.send_message(call.message.chat.id, f"â <b>DELIVERED</b> to {uid}\n{flag} {server_name}\nð± {phone}\nð° Cost â¹{web_price} | Sell â¹{bot_price} | <b>Profit â¹{PROFIT}</b>")
                else:
                    err=result.get("error","Unknown") if result else "No response"
                    bot.send_message(uid, f"â ï¸ Admin approved but API failed!\nError: {err}\n@just_zevric ko bolo!")
                    bot.send_message(call.message.chat.id, f"â API Failed {uid}: {err} | {server_name}")
            except Exception as e: bot.send_message(call.message.chat.id, f"Approve Error: {e}")
        elif d.startswith("rj_"):
            uid=int(d.split("_")[1]); bot.send_message(uid, "â Payment Rejected! Real screenshot bhejo!", parse_mode="HTML")
            bot.edit_message_text(f"â Rejected {uid} - Fake", call.message.chat.id, call.message.message_id); bot.answer_callback_query(call.id, "Rejected")
        elif d.startswith("go_"):
            uid=int(d.split("_")[1]); order_id=user_activations.get(uid)
            if not order_id: bot.send_message(uid, "â Order nahi mila!", parse_mode="HTML"); return
            bot.send_message(uid, f"ð Checking OTP... Order {order_id}\n10 sec wait...", parse_mode="HTML")
            otp=None
            for _ in range(12):
                otp=api_get_otp(order_id)
                if otp: break
                time.sleep(10)
            if otp: num=user_numbers.get(uid,""); bot.send_message(uid, f"ð <b>OTP READY! ð</b>\nð± {num}\nð OTP: <code>{otp}</code>\nâ¡ Jaldi daalo!", parse_mode="HTML"); bot.send_message(ADMIN_ID, f"â OTP to {uid}: {otp} | {num}")
            else: bot.send_message(uid, f"â³ OTP nahi aaya! Order {order_id}\n1 min baad try karo!", parse_mode="HTML")
            bot.answer_callback_query(call.id, "Checked!")
        elif d.startswith("cancel_"):
            order_id=d.split("_")[1]; res=api_cancel(order_id); bot.send_message(call.message.chat.id, f"Cancel {order_id}: {res}")
    except Exception as e: print(f"CB Error: {e}")

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    uid=message.from_user.id; server_name=user_selection.get(uid)
    if not server_name: bot.send_message(message.chat.id, "â ï¸ Pehle /buy se server select karo! ð±", parse_mode="HTML"); return
    web_price=WEBSITE_SERVERS.get(server_name,50); bot_price=web_price+PROFIT
    pending_orders[uid]={"server":server_name,"web_price":web_price,"bot_price":bot_price}
    flag,code=get_flag_code(server_name)
    username=f"@{message.from_user.username}" if message.from_user.username else "No username"; name=message.from_user.first_name or ""
    txt_admin=f"ð <b>NEW ORDER - VERIFY!</b>\nð¤ {name} {username} | {uid}\nð {flag} {server_name}\nð° Cost â¹{web_price} â Sell â¹{bot_price} = <b>Profit â¹{PROFIT}</b>\nServer: <code>{server_name}</code>\n\nâ ï¸ Check REAL payment!\nReal â â Approve\nFake â â Reject"
    bot.send_message(ADMIN_ID, txt_admin, parse_mode="HTML"); bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    mk=types.InlineKeyboardMarkup(row_width=2); mk.add(types.InlineKeyboardButton(f"â Approve â¹{bot_price} (Profit â¹{PROFIT})", callback_data=f"ap_{uid}_{server_name}"), types.InlineKeyboardButton("â Reject Fake", callback_data=f"rj_{uid}"))
    bot.send_message(ADMIN_ID, "Action:", reply_markup=mk)
    bot.send_message(message.chat.id, f"ð¸ Screenshot Received! â\n{flag} {server_name} - â¹{bot_price}\nð Admin verify kar raha hai (30 sec)...", parse_mode="HTML")

print(f"FINAL BOT - Hidden Profit - Commands Restored - Profit â¹{PROFIT} - STARTED")
app=Flask(__name__)
@app.route('/')
def home(): return f"Zevric Final - Hidden Profit â¹{PROFIT} - All Commands"
def run_web(): app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
threading.Thread(target=run_web).start()
bot.infinity_polling(skip_pending=True, timeout=10, long_polling_timeout=10, allowed_updates=["message","callback_query"], none_stop=True)
