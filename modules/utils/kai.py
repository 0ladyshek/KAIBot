from aiohttp import ClientSession
from config import kai_token
from yarl import URL
import json as js
from bs4 import BeautifulSoup as bs4

class KAI:
    def __init__(self, group: str = '', login: str = '', password: str = ''):
        self.group = group
        self.login = login
        self.password = password
        self.token = kai_token
        self.session = ClientSession(base_url=URL("https://schedule-bot.kai.ru/"))
        
    async def check_valid_group(self, group: str) -> bool:
        return bool((await self.requester(f"/api/schedule_public/groups", params = {"query": group})).get("result", {}).get("groups", []))
        
    async def close(self):
        return await self.session.close()
        
    async def auth(self, login: str = '', password: str = '') -> bool | str:
        if not (login and password) and not (self.login and self.password):
            return "Вы не ввели логин и пароль"
        if login and password:
            self.login = login
            self.password = password
        
        token = await self.requester(f"/api/registration", method = "POST", json = {"login": self.login, "password": self.password})
        if token.get("token"):
            self.token = token.get("token")
            return True
        return token.get('error')
    
    async def get_schedule(self) -> dict:
        return (await self.requester(f"/api/schedule_public/{self.group}"))
        
    async def get_exams(self) -> dict:
        return (await self.requester(f"/api/schedule_public/exam/{self.group}"))
        
    async def get_subjects_group(self) -> dict:
        return (await self.requester(f"/api/schedule_public/{self.group}/lessons"))
        
    async def filter_teacher(self, teacher: str) -> dict:
        return (await self.requester(f"/api/schedule_public/teachers", params = {"search": teacher}))
        
    async def get_schedule_teacher(self, teacher: str) -> dict:
        return (await self.requester(f"/api/schedule_public/teachers/{teacher}"))
        
    async def filter_group(self, group: str) -> dict:
        return (await self.requester(f"/api/schedule_public/groups", params = {"query": group}))
        
    async def get_students_list(self, group_id: str) -> list:
        self.session._base_url = URL("https://kai.ru/")
        self.token = None
        page = await self.requester("/infoClick/-/info/group", params = {"id": group_id}, output = "text")
        self.session._base_url = URL("https://schedule-bot.kai.ru/")
        page = bs4(page, "lxml").find("tbody")
        if not page: return []
        page = page.find_all("tr")
        if not page: return []
        students = []
        for i, row in enumerate(page):
            student = row.find_all("td")[1].text.replace("\n","").replace("  ", "").replace("Староста", " *(🙋Староста)*").strip()
            if not student: continue
            students.append(f"{i + 1}. {student}")
        return students
        
    async def requester(self, url: str = "/", method: str = "GET", json: dict = {}, params: dict = {}, output: str = "json") -> dict | str | bytes:
        if not params.get("token") and self.token:
            params["token"] = kai_token
        async with self.session.request(method, url, json=json, params=params, headers = {'User-Agent': 'python-requests/2.32.3', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': '*/*', 'Connection': 'keep-alive'}) as response:
            if output == "json":
                response = await response.text()
                return js.loads(response)
            elif output == "text":
                return await response.text()
            else:
                return await response.read()