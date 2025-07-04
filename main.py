import asyncio
import json
import logging
from datetime import datetime, timedelta

from aiogram.client.default import DefaultBotProperties
from aiohttp import ClientSession
from aiogram import Bot, Dispatcher, F, html
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import BOT_TOKEN
from db import set_subscription, get_subscription, init_db, set_invoice_uuid, get_invoice_uuid
from utils import generate_headers

dp = Dispatcher()


# ===== ОБРАБОТЧИК КОМАНТЫ СТАРТ =====
@dp.message(CommandStart())
async def start_handler(message: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💎 Купить подписку", callback_data="buy_subscription")],
        [InlineKeyboardButton(text="👤 Личный кабинет", callback_data="profile")]
    ])

    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!\n"
                         "Этот бот даёт доступ к премиум-контенту.\n"
                         "Нажми кнопку ниже, чтобы начать ⬇️", reply_markup=kb)


# ===== ОБРАБОТЧИК НАЖАТИЯ НА КНОПКУ ПОКУПКИ ПОДПИСКИ =====
@dp.callback_query(F.data == "buy_subscription")
async def create_payment(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    order_id = f"sub-{user_id}-{int(datetime.now().timestamp())}"

    payload = {
        "amount": "1",
        "currency": "TON",
        "order_id": order_id
    }
    json_data = json.dumps(payload)

    async with ClientSession() as session:
        response = await session.post(
            "https://api.heleket.com/v1/payment",
            headers=generate_headers(json_data),
            data=json_data
        )
        data = await response.json()

    uuid = data["result"]["uuid"]
    url = data["result"]["url"]

    await set_invoice_uuid(user_id, uuid)

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔁 Проверить оплату", callback_data=f"check_payment:{uuid}")]
    ])

    await callback.message.answer(f"Перейди по ссылке для оплаты:\n<a href='{url}'>{url}</a>",
                                  disable_web_page_preview=True,
                                  reply_markup=kb)


# ===== ОБРАБОТЧИК ПРОВЕРКИ НА ОСУЩЕСТВЛЕНИЕ ПЛАТЕЖА =====
@dp.message(Command("check"))
async def check_last_payment(message: Message):
    user_id = message.from_user.id
    uuid = await get_invoice_uuid(user_id)
    if not uuid:
        await message.answer("У вас нет активных платежей для проверки.")
        return

    json_data = json.dumps({"uuid": uuid})

    async with ClientSession() as session:
        response = await session.post(
            "https://api.heleket.com/v1/payment/info",
            headers=generate_headers(json_data),
            data=json_data
        )
        data = await response.json()

    status = data["result"]["status"]

    if status == "paid":
        until = datetime.now() + timedelta(days=30)
        await set_subscription(user_id, until.strftime("%Y-%m-%d"))
        await message.answer(f"✅ Оплата прошла успешно!\nПодписка активна до <b>{until.date()}</b>")
    else:
        await message.answer("⏳ Оплата не найдена. Попробуйте позже.")


# ===== ПРОВЕРКА ПЛАТЕЖА =====
@dp.callback_query(F.data.startswith("check_payment:"))
async def check_payment(callback: CallbackQuery):
    await callback.answer()
    uuid = callback.data.split(":")[1]

    json_data = json.dumps({"uuid": uuid})

    async with ClientSession() as session:
        response = await session.post(
            "https://api.heleket.com/v1/payment/info",
            headers=generate_headers(json_data),
            data=json_data
        )
        data = await response.json()

    status = data["result"]["status"]
    user_id = callback.from_user.id

    if status == "paid":
        until = datetime.now() + timedelta(days=30)
        await set_subscription(user_id, until.strftime("%Y-%m-%d"))
        await callback.message.answer("✅ Оплата прошла успешно!\n"
                                      f"Подписка активна до <b>{until.date()}</b>")
    else:
        await callback.message.answer("⏳ Оплата не найдена. Попробуйте позже.")


# ===== ЛИЧНЫЙ КАБИНЕТ =====
@dp.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    until = await get_subscription(user_id)

    if until:
        text = f"👤 Ваш профиль\n\n📅 Подписка активна до: <b>{until}</b>"
    else:
        text = "👤 Ваш профиль\n\n❌ Подписка не активна."

    await callback.message.answer(text)


# ===== ОБРАБОТЧИК ВСЕХ ОСТАЛЬНЫХ СООБЩЕНИЙ =====
@dp.message()
async def echo(message: Message):
    await message.answer("Напиши /start чтобы купить подписку или посмотреть профиль.")


async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
