import asyncio
from aiogram import Bot, Dispatcher, F
from config import Config
from aiogram.types import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import database 
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from logging import Logger

logger = Logger("bot")
bot = Bot(Config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.text == "/start")
async def start_command(message: Message):
    await message.answer("*Hi👋*", parse_mode="Markdown", reply_markup=main_menu())

@dp.message(F.text == "◀️ Cancel")
async def cancel_handler(message: Message, state: FSMContext):
    if state:
        await state.clear()
    
    await message.answer("Cancelled.", reply_markup=main_menu())

@dp.message(F.text == "ℹ️ Bot info")
async def get_info(message: Message):
    try:
        msg = ""
        source_chats = database.get_all_sources()
        msg += f"🎊 Source chats: {", ".join(source_chats)}\n"
        
        target_chat = database.get_target_chat()
        msg += f"🎯 Target chat: {str(target_chat) if target_chat is not None else "not setted!"}\n"

        spam_keywords = database.get_all_spam_keywords()
        print(spam_keywords)
        msg += f"⭕️ Spam keywords: {", ".join(spam_keywords)}\n"

        spam_types = database.get_all_spam_types()
        msg += f"⭕️ Spam types: {", ".join(spam_types)}\n"

        ai_info = database.get_ai_status()
        msg += f"🤖 AI model: {ai_info['model']}\n"
        msg += f"🟢 AI Enabled\n" if bool(ai_info['enabled']) else "🔴 AI Disabled\n"
        
        await message.answer(msg)
    except Exception as e:
        await message.answer("Something went wrong, please try again later.")

class AddSource(StatesGroup):
    username = State()

@dp.message(F.text == "➕ Add source")
async def add_source(message: Message, state: FSMContext):
    try:
        await state.set_state(AddSource.username)
        await message.answer("Enter username: ", reply_markup=cancel_keyboard())
    except Exception as e:
        logger.error(f"Error in add_source: {e}")

@dp.message(AddSource.username)
async def save_source(message: Message, state: FSMContext):
    try:
        username = message.text.strip()
        if not username.startswith("@"):
            await message.answer("Incorrect input!\nExample: @username_source", reply_markup=cancel_keyboard())
            return

        await state.clear()
        database.add_source(username)
        await message.answer("✅", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Error in save_source: {e}")

class RemoveSource(StatesGroup):
    username = State()

@dp.message(F.text == "❌ Del source")
async def del_source(message: Message, state: FSMContext):
    try:
        await state.set_state(RemoveSource.username)
        await message.answer("Enter username: ", reply_markup=cancel_keyboard())
    except Exception as e:
        logger.error(f"Error in add_source: {e}")

@dp.message(RemoveSource.username)
async def save_del_source(message: Message, state: FSMContext):
    try:
        username = message.text.strip()
        if not username.startswith("@"):
            await message.answer("Incorrect input!\nExample: @username_source", reply_markup=cancel_keyboard())
            return

        await state.clear()
        database.del_source(username)
        await message.answer("✅", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Error in del: {e}")

class TargetChat(StatesGroup):
    username = State()

@dp.message(F.text == "🎯 Set target chat")
async def set_target_chat(message: Message, state: FSMContext):
    try:
        await state.set_state(TargetChat.username)
        await message.answer("Enter the target chat username (e.g., @targetchannel):", reply_markup=cancel_keyboard())
    except Exception as e:
        logger.error(f"Error in set_target_chat: {e}")

@dp.message(TargetChat.username)
async def save_target_chat(message: Message, state: FSMContext):
    try:
        username = message.text.strip()
        if not username.startswith("@"):
            await message.answer("Incorrect input!\nExample: @targetchannel", reply_markup=cancel_keyboard())
            return

        database.set_target_chat(username)

        await state.clear()
        await message.answer("🎯 Target chat set successfully!", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Error in save_target_chat: {e}")


class AddSpamKeyword(StatesGroup):
    keyword = State()

@dp.message(F.text == "➕ Add spam keyword")
async def add_spam_keyword(message: Message, state: FSMContext):
    try:
        await state.set_state(AddSpamKeyword.keyword)
        await message.answer("Enter : ", reply_markup=cancel_keyboard())
    except Exception as e:
        logger.error(f"Error in add_source: {e}")

@dp.message(AddSpamKeyword.keyword)
async def save_spam_keyword(message: Message, state: FSMContext):
    try:
        keyword = message.text.strip()
        await state.clear()
        database.add_spam_keyword(keyword)
        await message.answer("✅", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Error in save_source: {e}")

class RemoveSpamKeyword(StatesGroup):
    keyword = State()

@dp.message(F.text == "❌ Del spam keyword")
async def del_spam_keyword(message: Message, state: FSMContext):
    try:
        await state.set_state(RemoveSpamKeyword.keyword)
        await message.answer("Enter : ", reply_markup=cancel_keyboard())
    except Exception as e:
        logger.error(f"Error in del_spam_keyword: {e}")

@dp.message(RemoveSpamKeyword.keyword)
async def save_spam_keywords(message: Message, state: FSMContext):
    try:
        keyword = message.text.strip()

        await state.clear()
        database.del_spam_keyword(keyword)
        await message.answer("✅", reply_markup=main_menu())
    except Exception as e:
        logger.error(f"Error in save_spam_keywords: {e}")

# Keyboards
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="ℹ️ Bot info")
            ],
            [
                KeyboardButton(text="🎯 Set target chat")
            ],
            [
                KeyboardButton(text="➕ Add source"), 
                KeyboardButton(text="❌ Del source")
            ],
            [
                KeyboardButton(text="➕ Add spam keyword"),
                KeyboardButton(text="❌ Del spam keyword")
            ],
            [
                KeyboardButton(text="➕ Add  spam type"),
                KeyboardButton(text="❌ Del spam type")
            ],
            [
                KeyboardButton(text="🟢 Enable AI"),
                KeyboardButton(text="🔴 Disable AI")
            ]
        ],
        resize_keyboard=True
    )

def cancel_keyboard():
    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text="◀️ Cancel")
            ]
        ]
    )

async def main():
    print("Starting....")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())