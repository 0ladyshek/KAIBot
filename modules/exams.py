from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.maria import Maria
from .utils.kai import KAI
from .utils.utils import format_exams

maria = Maria()

#text="Экзамены"
async def exams(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    exams = await kai.get_exams()
    await kai.close()
    if not exams.get("student_exams"):
        return await message_edit.edit_text("Экзамены не найдены")
    result = await format_exams(exams)
    if not result:
        return await message_edit.edit_text("Экзамены не найдены")
    await message_edit.edit_text(f"Экзамены в этом семестре:{result}", parse_mode="markdown")

def register(dp: Dispatcher):
    dp.register_message_handler(exams, text="Экзамены", state="*")