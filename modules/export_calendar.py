from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.maria import Maria
from .utils.kai import KAI
from .utils.keyboard import keyboard_export_calendar
from .utils.utils import export_schedule

maria = Maria()

#text="export_calendar"
async def export_calendar(message: types.CallbackQuery, state: FSMContext):
    await message.answer()
    await state.finish()
    await message.message.edit_text("Выберите период экспорта\n\nПри выборе большого периода, учитывайте, что расписание может быть изменено", reply_markup=keyboard_export_calendar)
    
#text_contains="export_calendar|"
async def export_calendar_callback(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.answer()
    await message.message.edit_text("Пожалуйста, подождите")
    period = message.data.split("|")[1]
    if period == "week":
        days = 7
    elif period == "2_week":
        days = 14
    elif period == "month":
        days = 30
    group = await maria.get_group_number(message.from_user.id)
    kai = KAI(group)
    schedule = await kai.get_schedule()
    await kai.close()
    if not schedule.get("result", {}).get("schedule"):
        return await message.message.edit_text("Расписание не найдено")
    result = await export_schedule(schedule, days)
    await message.message.answer_document(types.InputFile(result, filename="PersonalSchedule.ics"), caption="Расписание экспортировано в календарь")
    await message.message.delete()
    
def register(dp: Dispatcher):
    dp.register_callback_query_handler(export_calendar, text="export_calendar", state="*")
    dp.register_callback_query_handler(export_calendar_callback, text_contains="export_calendar|", state="*")