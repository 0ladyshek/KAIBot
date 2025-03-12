from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.keyboard import keyboard_donut

#text="Донат"
async def donut(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Поддержи разработчика донатом! Это поможет развивать экосистему бота и делать его более удобным для использования. Помни - бот существует только от поддержки подписчиков.", reply_markup=keyboard_donut)
    
def register(dp: Dispatcher):
    dp.register_message_handler(donut, text="Донат", state="*")