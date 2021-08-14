from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from cron import run_task
from common import Task, TaskModel
from uuid import uuid4

app = FastAPI()


class Response:

    @staticmethod
    def error(msg="", code=400):
        return HTTPException(status_code=code, detail=msg)

    @staticmethod
    def success(data=None, msg="Success!"):
        return {
            "code": 0,
            "msg": msg,
            "data": data
        }


origins = [
    "http://127.0.0.1:8080",
    "http://localhost",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


class LoginUser(BaseModel):
    username: str
    password: str


class MemTasks():
    def __init__(self):
        self.taskList = []

    def getTask(self, task_id) -> Task or None:
        for task in self.taskList:
            if task.id == task_id:
                return task
        return None

    def addTask(self, **kwargs):
        task = Task(**kwargs)
        self.taskList.append(task)
        return task

    def removeTask(self, task_id):
        task = self.getTask(task_id)
        if task:
            task.stop = True
            self.taskList.remove(task)
        else:
            raise ValueError("This task_id not find: %s" % task_id)

    def all(self):
        return [t.to_dict() for t in self.taskList]


db = MemTasks()


@app.post("/login")
async def login(item: LoginUser):
    print(item)
    return Response.success({"token": "sfde3d223d232d"})


@app.get("/list")
async def CronList():
    return Response.success(db.all())


@app.get("/log/{task_id}")
async def get_log(task_id: str):
    task = db.getTask(task_id)

    if task:
        result = task.to_dict()
        result.update({"stdout": task.stdout, "stderr": task.stderr})
        return Response.success(data=result)
    else:
        raise Response.error("没有这个任务")


@app.post("/add")
async def addTask(item: TaskModel):
    if item.run_time:
        cron_check = Task.check_cron(item.run_time)
        if not cron_check:
            raise Response.error("错误的Cron表达式")

    task = db.addTask(task_id=uuid4().hex,
                      name=item.name,
                      run_time=item.run_time,
                      second=item.second,
                      cmd=item.cmd,
                      status=item.status)
    if task.status:
        run_task(task)
    return Response.success(task.to_dict())


@app.get("/start")
async def stopTask(task_id: str):
    msg = "Success 启动成功"
    task = db.getTask(task_id)
    if task:
        if task.status:
            raise Response.error("任务重复启动")
        else:
            task.status = True
            run_task(task)
    else:
        raise Response.error("Error 没有这个任务")
    return Response.success()


@app.get("/stop")
async def stopTask(task_id: str):
    task = db.getTask(task_id)
    if task:
        if task.status:
            task.status = False
            task.next_time = ""
        else:
            raise Response.error("任务已经停止")
    else:
        raise Response.error("Error 没有这个任务")
    return Response.success()


@app.get("/del")
async def delTask(task_id: str):
    try:
        db.removeTask(task_id)
    except ValueError:
        raise Response.error("没有这个任务")
    return Response.success()
