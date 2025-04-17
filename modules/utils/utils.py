from datetime import datetime, timedelta
from config import week_days
from ics import Calendar, Event
from io import StringIO

async def format_schedule_day(schedule: dict, date: datetime) -> str:
    date_str = date.strftime("%d.%m")
    day = str(date.weekday() + 1)
    week_type = date.isocalendar()[1] % 2
    result = ""
    for lesson in schedule['result']['schedule']:
        if lesson['daynum'] != day: continue
        if lesson['daydate'] == "неч/чет" or lesson['daydate'] == "чет/неч": pass
        elif lesson['daydate'] and ('неч' in lesson['daydate'] or 'чет' in lesson['daydate']) and not (("чет" in lesson['daydate'] and week_type == 0) or ("неч" in lesson['daydate'] and week_type == 1)): continue
        elif lesson['daydate'] and not ("чет" in lesson['daydate'] or "неч" in lesson['daydate']) and date_str not in [date for date in lesson['daydate'].split() if date != "/"]: continue
        result += f"➤* {(lesson['daydate'] if ('чет' not in lesson['daydate'] or 'неч' not in lesson['daydate'] or lesson['daydate'] == 'неч/чет' or lesson['daydate'] == 'чет/неч') else date_str) if lesson['daydate'] else ''}* ⌛*{lesson['daytime']} {lesson['discipltype']}* {lesson['disciplname']} {lesson['auditory']} {lesson['building']} зд.\n"
    return result

async def export_schedule(schedule: dict, days: int) -> str:
    calendar = Calendar(creator="KAI Schedule Bot")
    for day in range(days + 1):
        date = datetime.now() + timedelta(days=day)
        date_str = date.strftime("%d.%m")
        date_str_calendar = date.strftime("%Y-%m-%d")
        week_type = date.isocalendar()[1] % 2
        day = str(date.weekday() + 1)
        for lesson in schedule['result']['schedule']:
            if lesson['daynum'] != day: continue
            if lesson['daydate'] == "неч/чет" or lesson['daydate'] == "чет/неч": pass
            elif lesson['daydate'] and ('неч' in lesson['daydate'] or 'чет' in lesson['daydate']) and not (("чет" in lesson['daydate'] and week_type == 0) or ("неч" in lesson['daydate'] and week_type == 1)): continue
            elif lesson['daydate'] and not ("чет" in lesson['daydate'] or "неч" in lesson['daydate']) and date_str not in [date for date in lesson['daydate'].split() if date != "/"]: continue
            start_time = (datetime.strptime(lesson['daytime'], "%H:%M") - timedelta(hours=3)).strftime("%H:%M")
            event = Event()
            event.name = f"{lesson['discipltype']} {lesson['disciplname']}"
            event.begin = f"{date_str_calendar} {start_time}"
            event.location = f"В {lesson['auditory']} ауд. {lesson['building']} зд."
            event.description = f"В {lesson['auditory']} ауд. {lesson['building']} зд."
            event.duration = {"hours": 1, "minutes": 30}
            calendar.events.add(event)
    calendar_file = StringIO()
    calendar_file.write(calendar.serialize())
    calendar_file.seek(0)
    return calendar_file

async def format_schedule_full(schedule: dict) -> str:
    result = ""
    last_day = None
    for lesson in schedule['result']['schedule']:
        if int(lesson['daynum']) != last_day:
            result += f"───────{week_days[int(lesson['daynum']) - 1]}───────\n"
            last_day = int(lesson['daynum'])
        result += f"➤* {lesson['daydate']}* ⌛*{lesson['daytime']} {lesson['discipltype']}* {lesson['disciplname']} {lesson['auditory']} {lesson['building']} зд.\n"
    return (await too_long_result(result))

async def too_long_result(result: str, group_size: int = 50) -> list:
    lines = result.split("\n")
    return ["\n".join(lines[i:i + group_size]) for i in range(0, len(lines), group_size)]

async def format_exams(exams: dict) -> str:
    result = ""
    for exam in exams['student_exams']:
        result += f"\n\n*{exam['disciplname']}* {exam['examdate']} в {exam['examtime']}\nПринимает: *{exam['prepodfio']}* в {exam['auditory']} {exam['building']} зд."
    return result

async def format_teachers(teachers: dict) -> str:
    result = ""
    teachers_list = {}
    for lesson in teachers["lessons"].values():
        if not teachers_list.get(lesson['prepodfio']): teachers_list[lesson['prepodfio']] = {"type": "", "subject": ""}
        teachers_list[lesson['prepodfio']]["type"] += f", {lesson['discipltype']}"
        teachers_list[lesson['prepodfio']]["subject"] += f", {lesson['disciplname']}"
    for teacher in teachers_list:
        result += f"─────────────────────\n👨‍🏫 |{teachers_list[teacher]['type'].strip(', ')}| *{teachers_list[teacher]['subject']}*\n`{teacher}`\n"
    return result

async def format_teacher_schedule(schedule: dict) -> str:
    result = ""
    last_day = None
    for lesson in schedule['teacher_schedule']:
        if int(lesson['daynum']) != last_day:
            result += f"───────{week_days[int(lesson['daynum']) - 1]}───────\n"
            last_day = int(lesson['daynum'])
        result += f"➤* {lesson['daydate']}* ⌛*{lesson['daytime']} {lesson['discipltype']}* {lesson['disciplname']} гр. {' '.join(lesson['group_list'])} ауд. {lesson['auditory']} {lesson['building']} зд.\n"
    return (await too_long_result(result))