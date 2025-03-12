from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from ..utils.maria import Maria
from ..utils.keyboard import keyboard_subscribe
from devtools import debug

maria = Maria()

class ChannelSubscribe(BaseMiddleware):
    def __init__(self):
        super(ChannelSubscribe, self).__init__()

    async def on_pre_process_message(self, message: types.Message, data: dict):
        channel_name = await maria.get_setting("channel")
        if not channel_name: return
        if not channel_name.startswith("@"): channel_name = f"@{channel_name}"
        if not (await message.bot.get_chat_member(channel_name, message.from_user.id)).is_chat_member():
            keyboard = await keyboard_subscribe(channel_name)
            await message.answer(f'Чтобы пользоваться ботом, вам необходимо подписаться на канал! {channel_name}', reply_markup=keyboard, parse_mode="markdown")
            raise CancelHandler() 
        return
 