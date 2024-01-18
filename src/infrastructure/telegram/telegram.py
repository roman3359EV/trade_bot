from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

from src.config.telegram import TelegramSettings
from src.infrastructure.telegram.decorators import session_close
from src.infrastructure.queue.worker import queue_app


class Telegram:
    def __init__(self, telegram_id: int):
        self.config = TelegramSettings()
        self.bot = Bot(token=self.config.token)
        self.telegram_id = telegram_id

    @session_close
    async def send_message(self, message: str):
        await self.bot.send_message(chat_id=self.telegram_id, text=message)

    @session_close
    async def send_message_with_actions(self, message: str, action: str, url: str):
        button = InlineKeyboardButton(text=f'{action.title()} order', url=url)
        greeting = InlineKeyboardMarkup(inline_keyboard=[[button]])

        await self.bot.send_message(chat_id=self.telegram_id, text=message, reply_markup=greeting)


@queue_app.task
def sync_send_message(telegram_id: int, message: str):
    bot = Telegram(telegram_id)
    coro = bot.send_message(message)
    asyncio.run(coro)


@queue_app.task
def sync_send_message_with_actions(telegram_id: int, message: str):
    bot = Telegram(telegram_id)
    coro = bot.send_message_with_actions(message)
    asyncio.run(coro)
