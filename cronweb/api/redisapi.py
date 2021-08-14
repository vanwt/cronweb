from fastapi import FastAPI
from uuid import uuid4
import aioredis
from cron import run_task
from common import Task, TaskModel

app = FastAPI()


class RedisTasks:
    def __init__(self, host, port, user=None, db=None, password=None):
        self.server = "redis://{0}:{1}".format(host, port)
        self.password = password

    async def getTask(self, task_id) -> Task:
        redis = await aioredis.create_redis(self.server, password=self.password)
        task = await redis.get(task_id, encoding="utf-8")
        return Task(task_id=task_id, **task)

    async def addTask(self, task_id=uuid4().hex, **kwargs) -> Task:
        redis = await aioredis.create_redis(self.server, password=self.password)
        task = Task(task_id=task_id, **kwargs)
        await redis.hmset_dict(task_id, task.to_dict())
        return task

    async def removeTask(self, task_id):
        redis = await aioredis.create_redis(self.server, password=self.password)
        await redis.delete(task_id)

    async def all(self):
        redis = await aioredis.create_redis(self.server, password=self.password)
        return await redis.keys("*")


db = RedisTasks(host="192.169.10.145", port=6379, password="admin123")


@app.get("/")
async def index():
    return {"tasks": await db.all()}


@app.get("/log/{task_id}")
async def get_log(task_id: str):
    task = await db.getTask(task_id)
    result = {"msg": "没有这个任务"}
    if task:
        result = task.to_dict()
    return result


@app.post("/add")
async def addTask(item: TaskModel):
    task = await db.addTask(**item.dict())
    if not task.stop:
        run_task(task)
    return {"msg": "Success", "data": task.to_dict()}


@app.get("/start")
async def stopTask(task_id: str):
    result = {"msg": "Success 启动成功"}
    task = await db.getTask(task_id)
    if task:
        if not task.stop:
            result = {"msg": "任务已经启动"}
        else:
            task.stop = False
            run_task(task)
    else:
        result = {"msg": "Error 没有这个任务"}
    return result


@app.get("/stop")
async def stopTask(task_id: str):
    result = {"msg": "Success 停止成功"}
    task = await db.getTask(task_id)
    if task:
        if task.stop:
            result = {"msg": "任务已经停止"}
        else:
            task.stop = True
    else:
        result = {"msg": "Error 没有这个任务"}
    return result


@app.get("/del")
async def delTask(task_id: str):
    await db.removeTask(task_id)
    return {
        "msg": "Success 停止成功"
    }
