from aiogram.dispatcher.filters.state import State, StatesGroup

class Registration(StatesGroup):
    group = State()
    login = State()
    password = State()
    
class BackCall(StatesGroup):
    message = State()   
    
class ChangeGroup(StatesGroup):
    group = State()
    
class OtherSchedule(StatesGroup):
    teacher = State()
    group = State()
    
class StudentsList(StatesGroup):
    group = State()