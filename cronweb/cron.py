import asyncio, sys
from common import Task

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()


async def run_command(task):
    proc = await asyncio.create_subprocess_shell(
        task.cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    if stdout:
        task.stdout = stdout.decode(errors="ignore").strip()

    if stderr:
        task.stderr = stderr.decode(errors="ignore").strip()


def run_task(task: Task):
    print("add cmd:%s" % task.cmd)

    async def run():
        err = 0
        while True:
            if not task.status:
                break
            try:
                print(111)
                await run_command(task)
            except Exception as e:
                err += 1
                task.stderr = str(e)
                if err >= 3:
                    task.stop = True
                    break
            await asyncio.sleep(task.get_next_seconds(), loop=loop)

    loop.create_task(run())
