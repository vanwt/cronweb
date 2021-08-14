from croniter import croniter
import datetime
import uuid

MONGO = True
MYSQL = True
REDIS = True



try:
    import aioredis
except ModuleNotFoundError as e:
    aioredis = e
    REDIS = False

try:
    import aiomysql
except ModuleNotFoundError as e:
    aiomysql = e
    MYSQL = False
else:
    class MysqlTasks():
        def __init__(self, host, user, password):
            self.host = host

try:
    import aiomongo
except ModuleNotFoundError as e:
    aiomongo = e
    MONGO = False


class Database:
    def __init__(self, db: str = None, **kwargs):
        if db == "redis":
            if not REDIS:
                raise aioredis
            self.db = RedisTasks(**kwargs)
        elif db == "mysql":
            if not MYSQL:
                raise aiomysql
            self.db = MysqlTasks(**kwargs)
        else:
            self.db = MemTasks(**kwargs)

    async def getTask(self, task_id):
        return await self.db.getTask(task_id)

    async def removeTask(self, task_id):
        await self.db.removeTask(task_id)

    async def addTask(self, **kwargs):
        task_id = uuid.uuid4().hex
        return await self.db.addTask(task_id=task_id, **kwargs)

    async def all(self):
        return await self.db.all()
