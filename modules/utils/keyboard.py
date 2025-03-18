from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

async def keyboard_subscribe(channel_name: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Подписаться", url=f"https://t.me/{channel_name[:1]}"))
    return keyboard

async def keyboard_back(data: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=data))
    return keyboard

async def keyboard_organizations(organizations_list: list) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    for organization in organizations_list:
        if not organization.get("site_url"): continue
        keyboard.add(InlineKeyboardButton(text=organization.get("name"), url=organization.get("site_url")))
    keyboard.add(InlineKeyboardButton(f"Назад", callback_data="other"))
    return keyboard

keyboard_main = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(KeyboardButton("На сегодня"), KeyboardButton("На завтра"))
keyboard_main.add(KeyboardButton("На послезавтра"), KeyboardButton("По дням"), KeyboardButton("Полностью"))
keyboard_main.add(KeyboardButton("Четность недели"), KeyboardButton("Экзамены"), KeyboardButton("Преподаватели"))
keyboard_main.add(KeyboardButton("Разное"), KeyboardButton("О боте"))
keyboard_main.add(KeyboardButton("Обратная связь"))

keyboard_registration = InlineKeyboardMarkup()
#keyboard_registration.add(InlineKeyboardButton(text="Студент", callback_data="registration|student"))
keyboard_registration.add(InlineKeyboardButton(text="Гость", callback_data="registration|guest"))

keyboard_schedule_days = InlineKeyboardMarkup()
keyboard_schedule_days.add(InlineKeyboardButton(text="Понедельник", callback_data="schedule|0"), InlineKeyboardButton(text="Вторник", callback_data="schedule|1"))
keyboard_schedule_days.add(InlineKeyboardButton(text="Среда", callback_data="schedule|2"), InlineKeyboardButton(text="Четверг", callback_data="schedule|3"))
keyboard_schedule_days.add(InlineKeyboardButton(text="Пятница", callback_data="schedule|4"), InlineKeyboardButton(text="Суббота", callback_data="schedule|5"))
keyboard_schedule_days.add(InlineKeyboardButton(text="Назад", callback_data="start"))

keyboard_back_call = InlineKeyboardMarkup()
keyboard_back_call.add(InlineKeyboardButton(text="Продолжить", callback_data="back_call"))
keyboard_back_call.add(InlineKeyboardButton(text="Назад", callback_data="start"))

keyboard_donut = InlineKeyboardMarkup()
keyboard_donut.add(InlineKeyboardButton(text="Отправить перевод", url="https://www.tinkoff.ru/collectmoney/crowd/dobrynin.ilya22/EIJCP35973/?short_link=7EDMYnSmO68&httpMethod=GET"))

keyboard_other = InlineKeyboardMarkup()
keyboard_other.add(InlineKeyboardButton("Расписание преподавателя", callback_data="schedule_teacher"))
keyboard_other.add(InlineKeyboardButton("Расписание другой группы", callback_data="schedule_group"))
keyboard_other.add(InlineKeyboardButton("Сменить группу", callback_data="change_group"), InlineKeyboardButton("Чат студентов", url="https://t.me/+8WYDQ7AmpfI4ZDVi"))
keyboard_other.add(InlineKeyboardButton("Одногруппники", callback_data="students"))
keyboard_other.add(InlineKeyboardButton("Другая группа", callback_data="students_other"))
keyboard_other.add(InlineKeyboardButton(f"Организации", callback_data="organizations"))
keyboard_other.add(InlineKeyboardButton("Назад", callback_data="start"))

keyboard_select_teacher_schedule = InlineKeyboardMarkup()
keyboard_select_teacher_schedule.add(InlineKeyboardButton("Выбрать преподавателя", switch_inline_query_current_chat=""))
keyboard_select_teacher_schedule.add(InlineKeyboardButton("Назад", callback_data="other"))

keyboard_select_group_schedule = InlineKeyboardMarkup()
keyboard_select_group_schedule.add(InlineKeyboardButton("Выбрать группу", switch_inline_query_current_chat=""))
keyboard_select_group_schedule.add(InlineKeyboardButton("Назад", callback_data="other"))

keyboard_select_group_schedule = InlineKeyboardMarkup()
keyboard_select_group_schedule.add(InlineKeyboardButton("Выбрать группу", switch_inline_query_current_chat=""))
keyboard_select_group_schedule.add(InlineKeyboardButton("Назад", callback_data="other"))

keyboard_select_group_list = InlineKeyboardMarkup()
keyboard_select_group_list.add(InlineKeyboardButton("Выбрать группу", switch_inline_query_current_chat=""))
keyboard_select_group_list.add(InlineKeyboardButton("Назад", callback_data="other"))