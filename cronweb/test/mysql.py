import aiomysql
import asyncio


async def execute(sql):
    conn = await aiomysql.connect(host="192.169.10.145", user="root", port="3306", password="topview")

    cur = await conn.cursor()

    await cur.execute(sql)
    result = await cur.fetchall()
    print(result)

    await cur.close()
    conn.close()



if __name__ == '__main__':
    tasks = [
        execute("show databases"),
    ]

    asyncio.get_event_loop().run_until_complete(asyncio.wait(tasks))
