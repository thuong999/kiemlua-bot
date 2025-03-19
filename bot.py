import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

# Thay token bot của bạn ở đây
TOKEN = "8039028794:AAHP9naaK2Th0g8LY2-In2c7K20-nDzQVFI"
bot = telebot.TeleBot(TOKEN)

# Danh sách kênh cần tham gia
REQUIRED_CHANNELS = ["@quangthuong200"]

# Danh sách user và số dư
user_balance = {}

# Hàm kiểm tra người dùng đã tham gia kênh chưa
def check_subscription(user_id):
    for channel in REQUIRED_CHANNELS:
        try:
            chat_member = bot.get_chat_member(channel, user_id)
            if chat_member.status in ['member', 'administrator', 'creator']:
                continue
            else:
                return False
        except Exception as e:
            return False
    return True

# Lệnh /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_balance[user_id] = user_balance.get(user_id, 0)

    markup = InlineKeyboardMarkup()
    btn_check = InlineKeyboardButton("✅ Kiểm tra & nhận thưởng", callback_data="check_task")
    markup.add(btn_check)

    bot.send_message(user_id, f"💰 Chào {message.chat.first_name}!\n"
                              "📌 Tham gia kênh sau để nhận thưởng:\n"
                              f"➡ {', '.join(REQUIRED_CHANNELS)}", reply_markup=markup)

# Xử lý nút kiểm tra nhiệm vụ
@bot.callback_query_handler(func=lambda call: call.data == "check_task")
def check_task(call):
    user_id = call.message.chat.id

    if check_subscription(user_id):
        reward = 1000  # Tiền thưởng mỗi lần hoàn thành nhiệm vụ
        user_balance[user_id] += reward
        bot.answer_callback_query(call.id, "✅ Bạn đã tham gia đủ kênh! Nhận thưởng 1000đ.")
        bot.send_message(user_id, f"💰 Số dư hiện tại: {user_balance[user_id]}đ")
    else:
        bot.answer_callback_query(call.id, "❌ Bạn chưa tham gia đủ kênh!")

# Lệnh /balance - Xem số dư
@bot.message_handler(commands=['balance'])
def check_balance(message):
    user_id = message.chat.id
    balance = user_balance.get(user_id, 0)
    bot.send_message(user_id, f"💰 Số dư của bạn: {balance}đ")

# Lệnh /withdraw - Rút tiền
@bot.message_handler(commands=['withdraw'])
def withdraw_request(message):
    user_id = message.chat.id
    balance = user_balance.get(user_id, 0)

    if balance < 5000:
        bot.send_message(user_id, "⚠ Số dư tối thiểu để rút là 5000đ!")
        return

    bot.send_message(user_id, "✅ Yêu cầu rút tiền đã được gửi đến admin. Chờ duyệt!")
    # Ở đây, bạn có thể thêm code để gửi thông báo đến admin.

# Chạy bot
bot.polling(none_stop=True)
