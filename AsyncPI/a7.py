import asyncio
import time
import math


async def move(servo, angle, seconds):
    startTime = time.perf_counter()
    startAngle = 90
    period = 0.05  # 50 ms per tick
    delta = (angle - startAngle) * period / seconds
    print("servo:%d endangle:%.2f sec:%.2f delta:%.2f" % (servo, angle, seconds, delta))
    while ((startAngle >= angle) and delta < 0) or (
        (startAngle <= angle) and delta > 0
    ):
        if servo == 3:
            print(
                "servo:%.2f angle:%.2f time:%.2f"
                % (servo, startAngle, time.perf_counter() - startTime)
            )
        startAngle += delta
        await asyncio.sleep(period - 0.005)
    print("Complete servo:%d time:%.2f" % (servo, time.perf_counter() - startTime))


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def count(num):
    for i in range(num):
        print(i)


async def main():
    task1 = asyncio.create_task(say_after(1, "hello"))

    task2 = asyncio.create_task(say_after(2, "world"))

    task3 = asyncio.create_task(count(10))

    task4 = asyncio.create_task(move(1, 50, 1))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2
    await task3
    await task4


print(f"finished at {time.strftime('%X')}")


async def main1():
    task5 = asyncio.create_task(move(1, 120, 0.5))
    await task5


async def action(actions):
    tasks = []
    for act in actions:
        print(act)
        tasks.append(asyncio.create_task(move(act[0], act[1], 3)))
    for task in tasks:
        await task


# asyncio.run(main())
# asyncio.run(main1())
asyncio.run(action([[5, 50], [4, 110], [2, 40], [3, 120]]))
