from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.keyboard import keyboard_other, keyboard_select_teacher_schedule, keyboard_select_group_schedule
from .utils.states import OtherSchedule
from .utils.kai import KAI
from .utils.utils import format_teacher_schedule, format_schedule_full

#text="schedule_teacher"
async def schedule_teacher(message: types.CallbackQuery, state: FSMContext):
    await OtherSchedule.teacher.set()
    await message.answer()
    await message.message.edit_text("Нажмите на кнопку ниже, чтобы выбрать преподавателя", reply_markup=keyboard_select_teacher_schedule)
    
#inline_query, state="OtherSchedule:teacher"
async def select_teacher(message: types.InlineQuery, state: FSMContext):
    results = []
    kai = KAI()
    teachers = await kai.filter_teacher(message.query)
    await kai.close()
    
    for teacher in teachers['teachers'][(int(message.offset) if message.offset else 0)*50:50]:
        results.append(types.InlineQueryResultArticle(
            id=teacher['id'],
            title=teacher['fio'],
            input_message_content=types.InputTextMessageContent(message_text=teacher['id'])
        ))

    await message.answer(results=results, cache_time=1, is_personal=True)
    
#state=OtherSchedule.teacher
async def get_teacher_schedule(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    kai = KAI()
    schedule = await kai.get_schedule_teacher(message.text)
    await kai.close()
    if not schedule.get("teacher_schedule"):
        return await message_edit.edit_text("Расписание не найдено")
    result = await format_teacher_schedule(schedule)
    await message_edit.delete()
    for row in result:
        await message.answer(row, parse_mode="markdown")
    
#text="schedule_group"
async def schedule_group(message: types.CallbackQuery, state: FSMContext):
    await OtherSchedule.group.set()
    await message.answer()
    await message.message.edit_text("Нажмите на кнопку ниже, чтобы выбрать группу", reply_markup=keyboard_select_group_schedule)
    
#inline_query, state="OtherSchedule:group"
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
    
#state=OtherSchedule.group
async def get_group_schedule(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    kai = KAI(message.text)
    schedule = await kai.get_schedule()
    await kai.close()
    if not schedule.get("result", {}).get("schedule"):
        return await message_edit.edit_text("Расписание не найдено")
    result = await format_schedule_full(schedule)
    await message_edit.delete()
    for row in result:
        await message.answer(row, parse_mode="markdown")
    

def register(dp: Dispatcher):
    dp.register_callback_query_handler(schedule_teacher, text="schedule_teacher", state="*")
    dp.register_inline_handler(select_teacher, state=OtherSchedule.teacher)
    dp.register_message_handler(get_teacher_schedule, state=OtherSchedule.teacher)
    dp.register_callback_query_handler(schedule_group, text="schedule_group", state="*")
    dp.register_inline_handler(select_group, state=OtherSchedule.group)
    dp.register_message_handler(get_group_schedule, state=OtherSchedule.group)