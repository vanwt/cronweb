from croniter import croniter, CroniterNotAlphaError, CroniterBadCronError
from datetime import datetime, timedelta
from pydantic import BaseModel


class Task:
    def __init__(self, name=None, cmd=None, task_id=None, run_time="", second=None, next_time=None,
                 status=True):
        self.id = task_id
        self.name = name
        self.cmd = cmd
        self.run_time = run_time
        self.second = second
        self.next_time = next_time
        self.stdout_list = []
        self.stderr_list = []
        self.status = status

    def get_next_seconds(self):
        """
        获取下次执行时间的秒数
        """
        if self.second:
            return self.second
        now = datetime.now()
        cron = croniter(self.run_time, now)
        return (cron.get_next(datetime) - now).total_seconds()

    def get_next_time(self):
        """
        获取下次执行时间
        """
        now = datetime.now()
        if self.second:
            return (now + timedelta(seconds=self.second)).strftime("%Y-%m-%d %H:%M")

        cron = croniter(self.run_time, now)
        return cron.get_next(datetime).strftime("%Y-%m-%d %H:%M")

    @property
    def stdout(self):
        return self.stdout_list

    @stdout.setter
    def stdout(self, value):
        self.stdout_list.append(value)

    @property
    def stderr(self):
        return self.stderr_list

    @stderr.setter
    def stderr(self, value):
        self.stderr_list.append(value)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "cmd": self.cmd,
            "run_time": self.run_time,
            "second": self.second,
            "next_time": self.get_next_time(),
            "status": "Running" if self.status else "Stopped"
        }

    @staticmethod
    def check_cron(run_time):
        now = datetime.now()
        try:
            croniter(run_time, now)
        except (CroniterNotAlphaError, CroniterBadCronError):
            return False
        return True


class TaskModel(BaseModel):
    name: str
    cmd: str
    run_time: str = ""
    second: int = 0
    status: bool = True
