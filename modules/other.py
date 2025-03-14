from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from .utils.keyboard import keyboard_other, keyboard_back, keyboard_organizations
from .utils.maria import Maria
from .utils.states import ChangeGroup
from .utils.kai import KAI

maria = Maria()

#text="Разное"
async def other(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Выберите действие", reply_markup=keyboard_other)
    
#text="other"
async def other_button(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.answer()
    await message.message.delete()
    await message.message.answer("Выберите действие", reply_markup=keyboard_other)
    
#text="change_group"
async def change_group(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.answer()
    keyboard = await keyboard_back("other")
    await ChangeGroup.group.set()
    await message.message.edit_text("Введите номер группы", reply_markup=keyboard)    
    
#state=ChangeGroup.group
async def change_group_group(message: types.Message, state: FSMContext):
    keyboard = await keyboard_back("change_group")
    if not message.text.isdigit():
        await message.answer("Введите номер группы", reply_markup=keyboard)
        return
    kai = KAI(message.text)
    result = await kai.check_valid_group(message.text)
    await kai.close()
    if not result:
        return await message.answer("Введите номер группы", reply_markup=keyboard)
    await maria.update_group_number(message.from_user.id, message.text)
    await message.answer("Группа успешно изменена", reply_markup=keyboard_other)
    
#text="organizations"
async def organizations(message: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await message.answer()
    await message.message.edit_text(f"Пожалуйста, подождите")
    kai = KAI()
    organizations_list = await kai.get_organizations()
    await kai.close()
    if not organizations_list.get("result"):
        await message.message.edit_text("Пока здесь пусто, но мы работаем над этим!", reply_markup=keyboard_other)
        return
    organizations_list: list = organizations_list.get("result")
    organizations_list.sort(key=lambda x: x.get("priority"))
    result = "\n".join(f"{i + 1}. [{organization.get('name')}]({organization.get('site_url', 'https://kai.ru')}) - {organization.get('description')}" for i, organization in enumerate(organizations_list))
    keyboard = await keyboard_organizations(organizations_list)
    await message.message.edit_text(f"Список действующих организаций КАИ:\n\n{result}", reply_markup=keyboard, parse_mode="markdown", disable_web_page_preview=True)
    
def register(dp: Dispatcher):
    dp.register_message_handler(other, text="Разное", state="*")
    dp.register_callback_query_handler(change_group, text="change_group", state="*")
    dp.register_message_handler(change_group_group, state=ChangeGroup.group)
    dp.register_callback_query_handler(other_button, text="other", state="*")
    dp.register_callback_query_handler(organizations, text="organizations", state="*")