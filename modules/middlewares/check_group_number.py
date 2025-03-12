from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from ..utils.maria import Maria
from ..utils.keyboard import keyboard_registration
from ..utils.kai import KAI

maria = Maria()

class CheckGroupNumber(BaseMiddleware):
    def __init__(self):
        super(CheckGroupNumber, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        dp: Dispatcher = Dispatcher.get_current()
        state = await dp.storage.get_state(user=message.from_user.id, chat=message.chat.id)
        if state: return
        user = await maria.user_exists(message.from_user.id)
        if not user[0]:
            await message.answer("Чтобы пользоваться ботом, вам необходимо авторизоваться", reply_markup=keyboard_registration)
            raise CancelHandler() 
        kai = KAI(user[0])
        result = await kai.check_valid_group(user[0])
        await kai.close()
        if not result:
            await message.answer("Чтобы пользоваться ботом, вам необходимо авторизоваться", reply_markup=keyboard_registration)
            raise CancelHandler() 
        return