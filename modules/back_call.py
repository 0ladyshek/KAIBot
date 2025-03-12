from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.states import BackCall
from .utils.keyboard import keyboard_back_call, keyboard_back
from .utils.maria import Maria

maria = Maria()

#text="Обратная связь"
async def back_call(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(f"Здесь ты можешь задать свой вопрос, предложить улучшение для бота или сообщить об ошибке. Учтите, что принимаются вопросы ТОЛЬКО по вопросом, касательно работы чат-бота. Я не отвечаю на вопросы, связанные с учебным процессом, я не знаю какая у вас группа и режим работы Здравпункта. Не тратьте свое и мое время - воспользуйтесь гуглом google.com . Нажми на кнопку продолжить, чтобы сделать обращение", reply_markup=keyboard_back_call)
    
#text="back_call"
async def back_call_message(message: types.CallbackQuery, state: FSMContext):
    await BackCall.message.set()
    await message.answer()
    keyboard = await keyboard_back("start")
    await message.message.edit_text("Введите текст вопроса. \nПрикрепляйте только фотографии с галочкой \"Сжать фотографии\"", reply_markup=keyboard)
    
#state=BackCall.message
async def back_call_message_text(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Спасибо за ваше обращение! Мы обязательно рассмотрим его и постараемся учесть ваши пожелания. Ждите ответа в ближайшее время.")
    admins = await maria.get_admins()
    for admin in admins:
        try:
            await message.forward(admin[0])
        except:
            continue
        
def register(dp: Dispatcher):
    dp.register_message_handler(back_call, text="Обратная связь", state="*")
    dp.register_callback_query_handler(back_call_message, text="back_call", state="*")
    dp.register_message_handler(back_call_message_text, content_types=types.ContentTypes.all(), state=BackCall.message)