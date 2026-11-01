import telebot
from telebot import types


bot = telebot.TeleBot("9018302678:AAGxFRzocmB6eVoculBjK-ZJs0etyOop4Gc")

# Har bir foydalanuvchining savatchasini saqlash uchun lug'at
user_carts = {}

# /start buyrug'i
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💻 Texnologiyalar katalogi")
    btn2 = types.KeyboardButton("🛒 Savatcham")
    btn3 = types.KeyboardButton("📞 Biz bilan bog'lanish")
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id, 
        f"Assalomu alaykum, {message.from_user.first_name}! 🛍\n"
        "Smart Up texnologiyalar internet-do'konining rasmiy botiga xush kelibsiz.\n"
        "Kerakli bo'limni tanlang:", 
        reply_markup=markup
    )

# Asosiy menyu xabarlari
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    
    if message.text == "💻 Texnologiyalar katalogi":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 Smartfonlar", callback_data="category_smartphones"),
            types.InlineKeyboardButton("💻 Noutbuklar", callback_data="category_laptops"),
            types.InlineKeyboardButton("⌚ Aqlli soatlar", callback_data="category_watches")
        )
        bot.send_message(chat_id, "Bizda mavjud bo'lgan texnologiya kategoriyalari:", reply_markup=markup)
        
    elif message.text == "🛒 Savatcham":
        # Foydalanuvchining savatchasini tekshiramiz
        if chat_id in user_carts and user_carts[chat_id]:
            cart_text = "🛒 **Sizning savatchangiz:**\n\n"
            total = 0
            for item in user_carts[chat_id]:
                cart_text += f"• {item['name']} — ${item['price']}\n"
                total += item['price']
            cart_text += f"\n**Jami:** ${total}"
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ Buyurtmani rasmiylashtirish", callback_data="checkout"))
            bot.send_message(chat_id, cart_text, parse_mode="Markdown", reply_markup=markup)
        else:
            bot.send_message(chat_id, "Sizning savatchangiz hozircha bo'sh. 📭")
        
    elif message.text == "📞 Biz bilan bog'lanish":
        bot.send_message(chat_id, "Menejer bilan bog'lanish: @Smartup_Admin\nTelefon: +998 88 804 07 27")
    else:
        bot.send_message(chat_id, "Iltimos, pastdagi tugmalardan foydalaning! 📲")

# Inline tugmalar boshqaruvi
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    
    # 1. Kategoriyalar
    if call.data == "category_smartphones":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🍏 iPhone 15 Pro - $1000", callback_data="phone_iphone15"),
            types.InlineKeyboardButton("🤖 Samsung Galaxy S24 - $900", callback_data="phone_samsung24"),
            types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_catalog")
        )
        bot.edit_message_text("📱 Smartfonlar katalogidan birini tanlang:", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data == "category_laptops":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💻 MacBook Air M2 - $1100", callback_data="laptop_mac"),
            types.InlineKeyboardButton("💻 Asus ROG Strix - $1300", callback_data="laptop_asus"),
            types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_catalog")
        )
        bot.edit_message_text("💻 Noutbuklar katalogidan birini tanlang:", chat_id, call.message.message_id, reply_markup=markup)

    elif call.data == "category_watches":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("⌚ Apple Watch Series 9 - $400", callback_data="watch_apple"),
            types.InlineKeyboardButton("⌚ Smart Watch Ultra - $150", callback_data="watch_ultra"),
            types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_catalog")
        )
        bot.edit_message_text("⌚ Aqlli soatlar katalogidan birini tanlang:", chat_id, call.message.message_id, reply_markup=markup)

    # 2. Mahsulot ma'lumotlari
    elif call.data == "phone_iphone15":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Savatchaga qo'shish", callback_data="add_iphone15"))
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="category_smartphones"))
        bot.edit_message_text("📱 **iPhone 15 Pro**\n\n- Xotira: 256GB\n- Narxi: $1000", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "phone_samsung24":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Savatchaga qo'shish", callback_data="add_samsung24"))
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="category_smartphones"))
        bot.edit_message_text("🤖 **Samsung Galaxy S24**\n\n- Xotira: 256GB\n- Narxi: $900", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "laptop_mac":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Savatchaga qo'shish", callback_data="add_mac"))
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="category_laptops"))
        bot.edit_message_text("💻 **MacBook Air M2**\n\n- RAM: 8GB, SSD: 256GB\n- Narxi: $1100", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "laptop_asus":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🛒 Savatchaga qo'shish", callback_data="add_asus"))
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="category_laptops"))
        bot.edit_message_text("💻 **Asus ROG Strix**\n\n- RAM: 16GB, SSD: 512GB\n- Narxi: $1300", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # 3. Savatchaga qo'shish amallari
    elif call.data.startswith("add_"):
        if chat_id not in user_carts:
            user_carts[chat_id] = []
            
        # Mahsulot turiga qarab savatchaga qo'shamiz
        product_info = {}
        if call.data == "add_iphone15":
            product_info = {"name": "iPhone 15 Pro", "price": 1000}
        elif call.data == "add_samsung24":
            product_info = {"name": "Samsung Galaxy S24", "price": 900}
        elif call.data == "add_mac":
            product_info = {"name": "MacBook Air M2", "price": 1100}
        elif call.data == "add_asus":
            product_info = {"name": "Asus ROG Strix", "price": 1300}
            
        user_carts[chat_id].append(product_info)
        bot.answer_callback_query(call.id, "Mahsulot savatchaga qo'shildi! ✅", show_alert=True)

    # 4. Buyurtmani rasmiylashtirish
    elif call.data == "checkout":
        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, "Buyurtmangiz qabul qilindi! 🚀 Menejer tez orada siz bilan bog'lanadi.")
        user_carts[chat_id] = [] # Savatchani tozalash

    # 5. Katalogga qaytish
    elif call.data == "back_to_catalog":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 Smartfonlar", callback_data="category_smartphones"),
            types.InlineKeyboardButton("💻 Noutbuklar", callback_data="category_laptops"),
            types.InlineKeyboardButton("⌚ Aqlli soatlar", callback_data="category_watches")
        )
        bot.edit_message_text("Bizda mavjud bo'lgan texnologiya kategoriyalari:", chat_id, call.message.message_id, reply_markup=markup)

# # Botni ishga tushirish
# print("Do'kon boti savatcha funksiyasi bilan ishlamoqda...")
bot.infinity_polling()