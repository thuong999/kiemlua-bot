import telebot

# Thay thế bằng token bot của bạn
TOKEN = "8039028794:AAHP9naaK2Th0g8LY2-In2c7K20-nDzQVFI"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào mừng bạn đến với bot kiếm xu!")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Danh sách lệnh: /start, /help")

bot.polling()
