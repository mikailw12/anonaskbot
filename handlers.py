from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import keyboards
from requests import add_user

handler = Router()

# Укажите свой Telegram ID
ADMIN_ID = '-1002224413709'  # Замените на ваш реальный ID

class MessageText(StatesGroup):
    text = State()
    reply = State()  # Для состояния ответа

bot_message_id = None

# Хранение сообщений с ID отправителя
messages = {}

@handler.message(CommandStart())
async def start(message: Message, command: CommandStart, state: FSMContext):

    global bot_message_id
    referrer_id = command.args  # Получаем ID владельца из диплинка

    if not referrer_id:
        # Если диплинк не содержит ID, отправляем ссылку владельцу
        await message.answer(
            f'🚀Начни получать анонимные сообщения прямо сейчас!\n\nТвоя ссылка:\n👉 t.me/anonimniyaskbot?start={message.from_user.id}\n\nРазмести эту ссылку ☝️ в описании профиля Telegram/TikTok/Instagram, чтобы начать получать анонимные сообщения 💬'
        )
    else:
        await add_user(message.from_user.id, message.from_user.username)
        # Сохраняем ID владельца в состоянии
        await state.update_data(referrer_id=referrer_id)
        await state.set_state(MessageText.text)

        # Отправляем сообщение, чтобы пользователь отправил текст
        sent_message = await message.answer(
            '🚀Здесь можно отправить анонимное сообщение человеку, который опубликовал эту ссылку\n\n✍️Напишите сюда всё, что хотите ему передать, и через несколько секунд он получит ваше 💬 сообщение, но не будет знать от кого',
            reply_markup=keyboards.cancelkb
        )
        bot_message_id = sent_message.message_id  # Сохраняем ID сообщения

@handler.message(MessageText.text)
async def yes_text(message: Message, state: FSMContext):
    if not message.text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
    else:
        # Получаем данные из состояния
        data = await state.get_data()
        referrer_id = data.get("referrer_id")
        user_text = message.text

        # Отправляем текст владельцу ссылки
        if referrer_id:
            sent_message = await message.bot.send_message(
                chat_id=referrer_id,
                text=f'Вам пришло новое анонимное сообщение:\n{user_text}\n\n↩️ Ответьте на это сообщение, чтобы отправить ответ анонимно.'
            )
            messages[sent_message.message_id] = message.from_user.id  # Сохраняем ID сообщения и отправителя

            await message.answer("Ваше сообщение отправлено!")

        # Отправляем текст админу с информацией о получателе и отправителе
        sender_username = message.from_user.username or "Неизвестно"
        recipient_chat = await message.bot.get_chat(referrer_id)
        recipient_username = recipient_chat.username or "Неизвестно"
        admin_text = (
            f"Новое анонимное сообщение:\n\n{user_text}\n\n"
            f"Отправитель: @{sender_username}\nПолучатель: @{recipient_username}"
        )
        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text
        )

        await state.clear()  # Очищаем состояние после отправки текста

@handler.message(F.reply_to_message)
async def handle_reply(message: Message):
    # Проверяем, что сообщение является ответом на анонимное сообщение
    original_message_id = message.reply_to_message.message_id
    if original_message_id in messages:
        sender_id = messages[original_message_id]  # Получаем ID отправителя

        # Отправляем ответ анонимному пользователю
        try:
            await message.bot.send_message(
                chat_id=sender_id,
                text=f"Ответ на ваше анонимное сообщение:\n\n{message.text}"
            )
            await message.answer("Ваш ответ был отправлен.")
        except Exception as e:
            await message.answer("Не удалось отправить ответ.")
            print(f"Ошибка при отправке ответа: {e}")
        
        # Удаляем информацию о сообщении после ответа
        del messages[original_message_id]

@handler.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery, state: FSMContext):
    global bot_message_id
    await callback.answer()  # Подтверждаем callback-запрос

    # Удаляем последнее сообщение бота
    if bot_message_id:
        await callback.bot.delete_message(chat_id=callback.message.chat.id, message_id=bot_message_id)
        bot_message_id = None  # Обнуляем ID сообщения после удаления

    await state.clear()
    await callback.message.answer("Отправка сообщения была отменена")
