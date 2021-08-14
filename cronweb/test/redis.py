import aioredis
import asyncio


async def execute(taskname, **kwargs):
    redis = await aioredis.create_redis("redis://192.169.10.145:6379", password="admin123")

    await redis.hmset_dict(taskname, **kwargs)
    result = await redis.hgetall(taskname, encoding="utf-8")
    print(result)

    redis.close()
    await redis.wait_closed()


if __name__ == '__main__':
    tasks = [
        execute("task1", name="aaa", next="0000", seconds=20),
        execute("task2", name="bbb", next="1111", seconds=5)
    ]

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
