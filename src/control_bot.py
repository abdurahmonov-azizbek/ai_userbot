import asyncio
from aiogram import Bot, Dispatcher, F
from config import Config
from aiogram.types import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import database 

bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer("*Hi👋*", parse_mode="Markdown", reply_markup=main_menu())

@dp.message(F.text == "ℹ️ Bot info")
async def get_info(message: Message):
    try:
        msg = ""
        source_chats = database.get_all_sources()
        msg += f"Source chats: {source_chats}\n"

        target_chat = database.get_target_chat()
        msg += f"Target chat: {target_chat}\n"

        


    except Exception as e:
        await message.answer("Something went wrong, please try again later.")

# Keyboards
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="ℹ️ Bot info")
            ],
            [
                KeyboardButton(text="➕ Add source"), 
                KeyboardButton(text="❌ Del source")
            ],
            [
                KeyboardButton(text="➕ Add keyword"),
                KeyboardButton(text="❌ Del keyword")
            ],
            [
                KeyboardButton(text="🟢 Enable AI"),
                KeyboardButton(text="🔴 Disable AI")
            ]
        ],
        resize_keyboard=True
    )

async def main():
    print("Starting....")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())