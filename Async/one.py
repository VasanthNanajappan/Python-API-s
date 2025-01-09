import asyncio

print("start")

async def task1(callback):
    print("Task1 is completed")
    await callback()

async def task2():
    print("Task2 is completed")

asyncio.run(task1(task2))

print("End")