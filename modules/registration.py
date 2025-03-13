from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.maria import Maria
from .utils.keyboard import keyboard_main, keyboard_back, keyboard_registration
from .utils.states import Registration
from .utils.kai import KAI
maria = Maria()

#text="registration|guest"
async def registration_guest(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.answer()
    keyboard = await keyboard_back("start")
    await Registration.group.set()
    await message.message.edit_text(f"Введите номер вашей группы", reply_markup=keyboard)
    
#state=Registration.group
async def registration_guest_group(message: types.Message, state: FSMContext):
    message_edit = await message.answer("Пожалуйста, подождите...")
    if not message.text.isdigit():
        await message_edit.delete()
        return await message.answer("Введите номер вашей группы")
    kai = KAI(message.text)
    result = await kai.check_valid_group(message.text)
    await kai.close()
    if not result:
        await message_edit.delete()
        return await message.answer("Вы ввели неверный номер группы")
    await maria.update_group_number(message.from_user.id, message.text)
    await message_edit.delete()
    await state.finish()
    await message.answer(f"Готово! Теперь вы можете пользоваться ботом", reply_markup=keyboard_main)
    
#text="registration|student"
async def registration_student(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.answer()
    keyboard = await keyboard_back("start")
    await Registration.login.set()
    await message.message.edit_text(f"Введите ваш логин от портала BlackBoard Learn", reply_markup=keyboard)
    
#state=Registration.login
async def registration_student_login(message: types.Message, state: FSMContext):
    await state.update_data(login = message.text)
    await Registration.next()
    keyboard = await keyboard_back("registration|student")
    await message.answer(f"Введите ваш пароль от портала BlackBoard Learn", reply_markup=keyboard)
    
#state=Registration.password
async def registration_student_password(message: types.Message, state: FSMContext):
    login = (await state.get_data()).get("login")
    await state.finish()
    kai = KAI(login=login, password=message.text)
    result = await kai.auth()
    if isinstance(result, str):
        return await message.answer(f'Ошибка авторизации: {result}\n\nПопробуйте ещё раз', reply_markup=keyboard_registration)
    await maria.set_login_and_password(message.from_user.id, login, message.text)
    await message.answer(f"Готово! Теперь вы можете пользоваться ботом", reply_markup=keyboard_main)
    
def register(dp: Dispatcher):
    dp.register_callback_query_handler(registration_guest, text="registration|guest", state="*")
    dp.register_message_handler(registration_guest_group, state=Registration.group)
    dp.register_callback_query_handler(registration_student, text="registration|student", state="*")
    dp.register_message_handler(registration_student_login, state=Registration.login)
    dp.register_message_handler(registration_student_password, state=Registration.password)