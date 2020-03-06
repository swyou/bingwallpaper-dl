import asyncio


async def dosomething():
    limit = 0
    while limit < 100:
        print("start")
        limit = limit + 1
        await asyncio.sleep(3)
        print("end")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    tasks = []
    tasks.append(dosomething())
    tasks.append(dosomething())
    tasks.append(dosomething())
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()