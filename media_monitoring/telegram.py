import asyncio
import json

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import BotBlocked, BotKicked, MessageNotModified

from media_monitoring.config import MEDIA_INFO, TELEGRAM_API_TOKEN
from media_monitoring.db import db

bot = Bot(token=TELEGRAM_API_TOKEN, parse_mode="MarkdownV2")
dp = Dispatcher(bot)


def escape_msg(msg):
    for ch in (
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ):
        msg = msg.replace(ch, f"\\{ch}")
    return msg


HELP_MESSAGE = """*МОНИТОРИНГ СМИ*
*НА СТАДИИ ТЕСТИРОВАНИЯ\\!\\!\\!*
Ищет цели в названии новостей\\.
Цели не чувствительны к регистру\\.
/help \\- Показать это сообщение
/media \\- Выбрать СМИ
/run \\- Запустить рассылку
/stop \\- Остановить рассылку
/status \\- Статус рассылки
/add ЦЕЛЬ \\- Добавить одну цель \\(2 \\- 40 символов\\), не больше 100 целей всего
/targets \\- Редактор целей
Если заблокируете бота, все настройки *СБРОСЯТСЯ*"""


@dp.message_handler(commands=["start", "help"])
async def help(message: types.Message):
    await bot.send_message(message.chat.id, HELP_MESSAGE)


@dp.message_handler(commands="run")
async def run(message: types.Message):
    await db.run(message.chat.id)
    await bot.send_message(message.chat.id, "*Рассылка запущена\\!*")


@dp.message_handler(commands="stop")
async def stop(message: types.Message):
    await db.stop(message.chat.id)
    await bot.send_message(message.chat.id, "*Рассылка приостановлена\\!*")


@dp.message_handler(commands="status")
async def status(message: types.Message):
    chat = await db.get_chat(message.chat.id)
    if chat.get("active"):
        await bot.send_message(message.chat.id, "*Рассылка запущена\\!*")
    else:
        await bot.send_message(message.chat.id, "*Рассылка приостановлена\\!*")


def get_targets_keyboard_markup(targets):
    ch = "\u274c"
    return InlineKeyboardMarkup(
        1,
        [
            [
                InlineKeyboardButton(
                    f"{target} {ch}", callback_data=f"target:{target}"
                ),
            ]
            for target in targets
        ],
    )


@dp.message_handler(commands=["targets"])
async def show_list(message: types.Message):
    targets = await db.get_targets(message.chat.id)
    targets_count = len(targets)
    if targets_count == 0:
        await bot.send_message(message.chat.id, "Нет ни одной цели")
    else:
        await bot.send_message(
            message.chat.id,
            f"Число целей: {targets_count}",
            reply_markup=get_targets_keyboard_markup(targets),
        )


@dp.message_handler(commands="add")
async def add(message: types.Message):
    args = message.get_args().strip()

    if len(args) > 40 or len(args) < 2:
        await bot.send_message(message.chat.id, "*от 2 до 40 символов*")
        return
    # TODO: raise exception
    res = await db.update_targets(message.chat.id, args)
    await bot.send_message(message.chat.id, f"Цель *{args}* успешно добавлена\\!")


def get_media_keyboard_markup(users_media):
    res = []
    for id, title in MEDIA_INFO:
        ch = "\u2705" if id in users_media else "\u274c"
        res.append([InlineKeyboardButton(f"{title} {ch}", callback_data=f"media:{id}")])
    return InlineKeyboardMarkup(1, res)


@dp.message_handler(commands="media")
async def handle_media(message: types.Message):
    users_media = await db.get_media(message.chat.id)
    await bot.send_message(
        message.chat.id,
        f"*Выбрать СМИ*\nВыбрано источников: {len(users_media)}",
        reply_markup=get_media_keyboard_markup(users_media),
    )


@dp.callback_query_handler()
async def handle_callback(cq: types.CallbackQuery):
    data = json.loads(cq.as_json())
    chat_id = data.get("message").get("chat").get("id")
    message_id = data.get("message").get("message_id")
    callback_data = data.get("data")

    if callback_data is None:
        return

    is_media = callback_data.startswith("media")
    is_target = callback_data.startswith("target")

    if is_media:
        _, id = callback_data.split(":", 1)
        updated_media = await db.update_media(chat_id, int(id))
        await bot.edit_message_text(
            f"*Выбрать СМИ*\nВыбрано источников: {len(updated_media)}",
            chat_id,
            message_id,
        )
        await bot.edit_message_reply_markup(
            chat_id, message_id, reply_markup=get_media_keyboard_markup(updated_media)
        )
        return
    if is_target:
        _, target = callback_data.split(":", 1)
        updated_targets = await db.update_targets(chat_id, target)
        updated_targets_count = len(updated_targets)
        if updated_targets_count == 0:
            await bot.edit_message_text("Нет ни одной цели", chat_id, message_id)
            try:
                await bot.edit_message_reply_markup(
                    chat_id, message_id, reply_markup=None
                )
            except MessageNotModified:
                pass
        else:
            await bot.edit_message_text(
                f"Число целей: {updated_targets_count}", chat_id, message_id
            )
            await bot.edit_message_reply_markup(
                chat_id,
                message_id,
                reply_markup=get_targets_keyboard_markup(updated_targets),
            )
        return


def start_bot(loop):
    executor.start_polling(
        dp, loop=loop, skip_updates=True, on_shutdown=(db.close_connection,)
    )


async def send_notification(chat_id, msg):
    try:
        await bot.send_message(chat_id, msg)
    except (BotBlocked, BotKicked):
        pass
        # remove chat from db
        asyncio.create_task(db.delete_chat(chat_id))
