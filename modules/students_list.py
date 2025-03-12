from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .utils.maria import Maria
from .utils.kai import KAI
from .utils.keyboard import keyboard_back, keyboard_select_group_list
from .utils.states import StudentsList

maria = Maria()

#text="students"
async def students(message: types.CallbackQuery, state: FSMContext):
    await message.answer()
    await message.message.edit_text(f"Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI()
    group_id = (await kai.filter_group(group))['result']['groups'][0]['id']
    students = await kai.get_students_list(group_id)
    await kai.close()
    if not students:
        return await message.message.edit_text("Студенты не найдены")
    await message.message.edit_text("Студенты группы:\n\n" + "\n".join(students), parse_mode="markdown")
    
    users = await maria.get_users_by_group(group)
    result = "Ссылки на одногруппников:\n\n"
    for user in users:
        try:
            user = await message.bot.get_chat(user[0])
            result += f"[{user.full_name}]({f'tg://user?id={user.id}' if not user.username else f'https://t.me/{user.username}'})\n"
        except:
            continue
    await message.message.answer(result, parse_mode="markdown", disable_web_page_preview=True)
    
#text="students_other"
async def students_other(message: types.CallbackQuery, state: FSMContext):
    await message.answer()
    await message.message.edit_text("Нажмите на кнопку ниже, чтобы выбрать группу", reply_markup=keyboard_select_group_list)
    await StudentsList.group.set()
    
#state=StudentsList.group
async def students_other_group(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer()
    keyboard = await keyboard_back("students_other")
    await message.message.edit_text(f"Пожалуйста, подождите...", reply_markup=keyboard)

#inline_query, state="StudentsList:group"
async def select_group(message: types.InlineQuery, state: FSMContext):
    results = []
    kai = KAI()
    groups = await kai.filter_group(message.query)
    await kai.close()
    
    for group in groups['result']['groups'][(int(message.offset) if message.offset else 0)*50:50]:
        results.append(types.InlineQueryResultArticle(
            id=group['id'],
            title=group['groupNum'],
            input_message_content=types.InputTextMessageContent(message_text=group['groupNum'])
        ))

    await message.answer(results=results, cache_time=1, is_personal=True)
    
#state=StudentsList.group
async def get_students_list(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    kai = KAI()
    group_id = (await kai.filter_group(message.text))['result']['groups'][0]['id']
    students = await kai.get_students_list(group_id)
    await kai.close()
    if not students:
        return await message_edit.edit_text("Студенты не найдены")
    await message_edit.edit_text("Студенты группы:\n\n" + "\n".join(students), parse_mode="markdown")
    
    users = await maria.get_users_by_group(message.text)
    result = "Ссылки:\n\n"
    for user in users:
        try:
            user = await message.bot.get_chat(user[0])
            result += f"[{user.full_name}]({f'tg://user?id={user.id}' if not user.username else f'https://t.me/{user.username}'})\n"
        except:
            continue
    await message.answer(result, parse_mode="markdown", disable_web_page_preview=True)

def register(dp: Dispatcher):
    dp.register_callback_query_handler(students, text="students", state="*")
    dp.register_callback_query_handler(students_other, text="students_other", state="*")
    dp.register_inline_handler(select_group, state=StudentsList.group)
    dp.register_message_handler(get_students_list, state=StudentsList.group)