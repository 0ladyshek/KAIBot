from asyncmy import connect
from config import db_data

class Maria:
    def __init__(self):
        self.hostname = db_data[0]
        self.user = db_data[1]
        self.password = db_data[2]
        self.db = db_data[3]

    async def start_db(self):
        await self.connector(f"CREATE TABLE IF NOT EXISTS users(user_id BIGINT, group_number INT, login TEXT, password TEXT, admin INT)", commit = True)

    async def user_exists(self, user_id: int, login: str = '', password: str = '') -> bool:
        user = await self.connector(f"SELECT group_number FROM users WHERE user_id = %(user_id)s", {"user_id": user_id})
        if bool(len(user)):
            return user[0]
        await self.connector(f"INSERT INTO users VALUES(%(user_id)s, 0, %(login)s, %(password)s, 0)", {"user_id": user_id, "login": login, "password": password}, commit = True)
        return [0, '', '']
    
    async def set_login_and_password(self, user_id: int, login: str, password: str):
        await self.connector(f"UPDATE users SET login = %(login)s, password = %(password)s WHERE user_id = %(user_id)s", {"user_id": user_id, "login": login, "password": password}, commit = True)
    
    async def update_group_number(self, user_id: int, group: str):
        await self.connector(f"UPDATE users SET group_number = %(group_number)s WHERE user_id = %(user_id)s", {"user_id": user_id, "group_number": group}, commit = True)

    async def get_group_number(self, user_id: int) -> str:
        return (await self.connector(f"SELECT group_number FROM users WHERE user_id = %(user_id)s", {"user_id": user_id}))[0][0]

    async def get_admins(self) -> list:
        return await self.connector(f"SELECT user_id FROM users WHERE admin = 1")
    
    async def get_users_by_group(self, group: str) -> list:
        return await self.connector(f"SELECT user_id FROM users WHERE group_number = %(group_number)s", {"group_number": group})
    
    async def get_users(self) -> list:
        return await self.connector(f"SELECT COUNT(user_id) FROM users")
    
    async def connector(self, sql: str, args: dict = {}, commit: bool = False):
        async with connect(host=self.hostname, user=self.user, password=self.password, db=self.db, echo=True) as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(sql, args)
                if commit:
                    await connection.commit()
                    return True
                else:
                    return (await cursor.fetchall())