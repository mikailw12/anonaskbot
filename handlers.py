from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from keyboards import cancelkb

router = Router()

ADMIN_ID = '-1002224413709'  # Замените на ваш реальный ID

class MessageText(StatesGroup):
    text = State()
    reply = State()  # Для состояния ответа

bot_message_id = None
messages = {}

@router.message(CommandStart())
async def start(message: Message, command: CommandStart, state: FSMContext):
    global bot_message_id
    referrer_id = command.args

    if not referrer_id:
        await message.answer(
            f'🚀Начни получать анонимные сообщения прямо сейчас!\n\nТвоя ссылка:\n👉 t.me/anonimniyaskbot?start={message.from_user.id}\n\nРазмести эту ссылку ☝️ в описании профиля Telegram/TikTok/Instagram, чтобы начать получать анонимные сообщения 💬'
        )
    else:
        await state.update_data(referrer_id=referrer_id)
        await state.set_state(MessageText.text)
        sent_message = await message.answer(
            '🚀Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку\n\n✍️Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше 💬 сообщение, но не будет знать от кого',
            reply_markup=cancelkb
        )
        bot_message_id = sent_message.message_id

@router.message(MessageText.text)
async def yes_text(message: Message, state: FSMContext):
    data = await state.get_data()
    referrer_id = data.get("referrer_id")

    # Проверка наличия фотографии в сообщении
    if message.photo:
        photo = message.photo[-1].file_id  # Берём фотографию самого большого размера
        caption = message.caption or ""  # Подпись (если есть)
    else:
        photo = None
        caption = message.text or ""

    # Отправка сообщения владельцу
    if referrer_id:
        if photo:
            # Отправка фото с подписью
            sent_message = await message.bot.send_photo(
                chat_id=referrer_id,
                photo=photo,
                caption=f'Вам пришло новое анонимное сообщение:\n{caption}\n\n↩️ Ответьте на это сообщение, чтобы отправить ответ анонимно.'
            )
        else:
            # Отправка только текста
            sent_message = await message.bot.send_message(
                chat_id=referrer_id,
                text=f'Вам пришло новое анонимное сообщение:\n{caption}\n\n↩️ Ответьте на это сообщение, чтобы отправить ответ анонимно.'
            )

        messages[sent_message.message_id] = message.from_user.id
        await message.answer("Ваше сообщение отправлено!")

    # Отправка админу информации о сообщении
    sender_username = message.from_user.username or "Неизвестно"
    recipient_chat = await message.bot.get_chat(referrer_id)
    recipient_username = recipient_chat.username or "Неизвестно"
    admin_text = (
        f"Новое анонимное сообщение от @{sender_username} для @{recipient_username}:\n\n{caption}"
    )

    if photo:
        # Если есть фото, отправляем его администратору
        await message.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo,
            caption=admin_text
        )
    else:
        # Если фото нет, отправляем только текст
        await message.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

    await state.clear()


@router.message(F.reply_to_message)
async def handle_reply(message: Message):
    original_message_id = message.reply_to_message.message_id
    if original_message_id in messages:
        sender_id = messages[original_message_id]

        try:
            await message.bot.send_message(
                chat_id=sender_id,
                text=f"Ответ на ваше анонимное сообщение:\n\n{message.text}"
            )
            await message.answer("Ваш ответ был отправлен.")
        except Exception as e:
            await message.answer("Не удалось отправить ответ.")
            print(f"Ошибка при отправке ответа: {e}")
        
        del messages[original_message_id]

@router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    global bot_message_id
    await callback.answer()

    if bot_message_id:
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=bot_message_id)
        bot_message_id = None

    await state.clear()
    await callback.message.answer("Отправка сообщения была отменена")