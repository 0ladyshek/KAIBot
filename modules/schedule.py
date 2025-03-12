from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.maria import Maria
from .utils.keyboard import keyboard_main, keyboard_back, keyboard_schedule_days
from .utils.kai import KAI
from .utils.utils import format_schedule_day, format_schedule_full
from config import week_days
from datetime import datetime, timedelta

maria = Maria()

#text="На сегодня"
async def schedule_today(message: types.Message, state: FSMContext):    
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    schedule = await kai.get_schedule()
    await kai.close()
    if not schedule.get("result", {}).get("schedule"):
        return await message_edit.edit_text("Расписание на сегодня не найдено")
    date = datetime.now()
    result = await format_schedule_day(schedule, date)
    if not result:
        return await message_edit.edit_text("Расписание на сегодня не найдено")
    result = f"Расписание на сегодня:\n{result}"
    await message_edit.edit_text(result, parse_mode="markdown")
    
#text="На завтра"
async def schedule_tomorrow(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    schedule = await kai.get_schedule()
    await kai.close()
    if not schedule.get("result", {}).get("schedule"):
        return await message_edit.edit_text("Расписание на завтра не найдено")
    date = datetime.now() + timedelta(days=1)
    result = await format_schedule_day(schedule, date)
    if not result:
        return await message_edit.edit_text("Расписание на завтра не найдено")
    result = f"Расписание на завтра:\n{result}"
    await message_edit.edit_text(result, parse_mode="markdown") 
    
#text="На послезавтра"
async def schedule_after_tomorrow(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    schedule = await kai.get_schedule()
    await kai.close()
    if not schedule.get("result", {}).get("schedule"):
        return await message_edit.edit_text("Расписание на послезавтра не найдено")
    date = datetime.now() + timedelta(days=2)
    result = await format_schedule_day(schedule, date)
    if not result:
        return await message_edit.edit_text("Расписание на послезавтра не найдено")
    result = f"Расписание на послезавтра:\n{result}"
    await message_edit.edit_text(result, parse_mode="markdown") 
    
#text="По дням"
async def schedule_by_days(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберите день недели", reply_markup=keyboard_schedule_days)

#text_contains="schedule|"
async def schedule_by_days_callback(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.message.edit_text("Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    schedule = await kai.get_schedule()
    await kai.close()
    if not schedule.get("result", {}).get("schedule"):
        return await message.message.edit_text("Расписание на выбранный день не найдено")
    now = datetime.now()
    from_day = now.weekday()
    search_day = int(message.data.split("|")[1])
    different_days = search_day - from_day if from_day < search_day else 7 - from_day + search_day
    date = now + timedelta(days=different_days)
    result = await format_schedule_day(schedule, date)
    if not result:
        return await message.message.edit_text("Расписание на выбранный день не найдено")
    result = f"Расписание на _ближайшую(ий)_ *{week_days[search_day]}*:\n{result}"
    await message.message.edit_text(result, parse_mode="markdown")
    
#text="Полностью"
async def schedule_full(message: types.Message, state: FSMContext):
    await state.finish()
    message_edit = await message.answer("Пожалуйста, подождите...")
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    schedule = await kai.get_schedule()
    await kai.close()
    if not schedule.get("result", {}).get("schedule"):
        return await message_edit.edit_text("Расписание на выбранный день не найдено")
    result = await format_schedule_full(schedule)
    if not result:
        return await message_edit.edit_text("Расписание не найдено")
    await message_edit.delete()
    for row in result:
        await message.answer(row, parse_mode="markdown")
    
#text="Четность недели"
async def schedule_even_week(message: types.Message, state: FSMContext):
    await state.finish()
    week_type = datetime.now().isocalendar()[1] % 2
    await message.answer(f"Сейчас *{'нечетная' if week_type == 1 else 'четная'}* неделя", parse_mode="markdown")

def register(dp: Dispatcher):
    dp.register_message_handler(schedule_today, text="На сегодня", state="*")
    dp.register_message_handler(schedule_tomorrow, text="На завтра", state="*")
    dp.register_message_handler(schedule_after_tomorrow, text="На послезавтра", state="*")
    dp.register_message_handler(schedule_by_days, text="По дням", state="*")
    dp.register_callback_query_handler(schedule_by_days_callback, text_contains="schedule|", state="*")
    dp.register_message_handler(schedule_full, text="Полностью", state="*")
    dp.register_message_handler(schedule_even_week, text="Четность недели", state="*")