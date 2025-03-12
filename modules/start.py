from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.maria import Maria
from .utils.keyboard import keyboard_main, keyboard_registration

maria = Maria()

#commands=['start']
async def start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Добро пожаловать в главное меню", reply_markup=keyboard_main)

#text="start"
async def start_button(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.answer()
    await message.message.delete()
    await message.message.answer(f"Добро пожаловать в главное меню", reply_markup=keyboard_main)
    
def register(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_callback_query_handler(start_button, text="start", state="*")