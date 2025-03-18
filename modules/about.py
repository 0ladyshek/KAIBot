from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.maria import Maria

maria = Maria()

#text="О боте"
async def about(message: types.Message, state: FSMContext):
    await state.finish()
    users = await maria.get_users()
    await message.answer(f"Всего пользователей: {users[0][0]}\n\nНаш сервис позволяет вам получать свое расписание в удобной для вас форме. А так же: получать расписание других групп и ваших преподавателей, смотреть расписание экзаменов, узнать список студентов другой группы, и это только начало! Дальше - больше\n\n*Бот создан @oladushik, при поддержке @botkainews и @capy_para \nАвтор идеи @dobryninilya*", parse_mode="markdown")
    
def register(dp: Dispatcher):
    dp.register_message_handler(about, text="О боте", state="*")
