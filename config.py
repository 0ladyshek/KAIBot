import os

api_token = os.getenv("API_TOKEN")
kai_token = os.getenv("KAI_TOKEN")

db_data = ("db", os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_NAME"))

week_days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]