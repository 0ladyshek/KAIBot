from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.maria import Maria
from .utils.kai import KAI
from .utils.utils import format_teachers

maria = Maria()

#text="Преподаватели"
async def teachers(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    teachers = await kai.get_subjects_group()
    await kai.close()
    if not teachers.get("lessons"):
        return await message_edit.edit_text("Преподаватели не найдены")
    result = await format_teachers(teachers)
    if not result:
        return await message_edit.edit_text("Преподаватели не найдены")
    await message_edit.edit_text(f"Список преподавателей:\n{result}", parse_mode="markdown")
    
def register(dp: Dispatcher):
    dp.register_message_handler(teachers, text="Преподаватели", state="*")