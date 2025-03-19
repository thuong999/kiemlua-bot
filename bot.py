import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Thông tin bot
TOKEN = "8039028794:AAHP9naaK2Th0g8LY2-In2c7K20-nDzQVFI"
ADMIN_ID = 7790939467  # Thay bằng ID admin của bạn
API_KEY_THEGIARE = "YOUR_THEGIARE_API_KEY"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

# Hàm gọi API rút tiền từ TheGiare
def rut_tien(so_dien_thoai, so_tien):
    url = "https://api.thegiare.com/v1/withdraw"
    payload = {
        "api_key": API_KEY_THEGIARE,
        "phone": so_dien_thoai,
        "amount": so_tien
    }
    response = requests.post(url, json=payload)
    return response.json()

# Gửi menu chính khi user nhập /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("👉 Tham Gia Kênh 👈", url="https://t.me/example"),
        InlineKeyboardButton("✅ Check Nhận Code", callback_data="check_code"),
        InlineKeyboardButton("💳 Rút Tiền", callback_data="rut_tien")
    )

    await message.reply("🎁 Vui lòng tham gia kênh để nhận code!", reply_markup=keyboard)

# Xử lý check nhận code
@dp.callback_query_handler(lambda call: call.data == "check_code")
async def check_code(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "✅ Code của bạn là: ABC123")

# Xử lý rút tiền
@dp.callback_query_handler(lambda call: call.data == "rut_tien")
async def ask_for_withdrawal(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "💰 Nhập lệnh /rut [SĐT] [Số tiền] để rút tiền.")

@dp.message_handler(commands=['rut'])
async def rut_tien_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.reply("❌ Bạn không có quyền rút tiền!")
        return

    args = message.text.split()
    if len(args) < 3:
        await message.reply("❌ Sai cú pháp! Dùng: /rut [SĐT] [Số tiền]")
        return
    
    so_dien_thoai = args[1]
    so_tien = args[2]
    
    result = rut_tien(so_dien_thoai, so_tien)
    await message.reply(f"🔄 Đang xử lý rút tiền...\n📢 Kết quả: {result}")

# Chạy bot
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)