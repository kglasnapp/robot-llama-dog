import asyncio
import time
import select
import sys

#from terminedia import ainput

def charAvailable():
    return select.select([sys.stdin], [], [], 0)[0]

async def func1():
	print("Function 1 started..")
	await asyncio.sleep(2)
	print("Function 1 Ended")


async def func2():
    count = 0
    start = time.perf_counter()
    while True:
      print("Function 2 started..", time.perf_counter() - start)
      await asyncio.sleep(2)
      count += 1
      if count > 20:
          break
  


async def func3():
    print("Function 3 started..")
    while True:
      if charAvailable():
        print("func3", "char found")
        break
    await asyncio.sleep(.1)

    print("Function 3 Ended")


async def main():
	L = await asyncio.gather(
		func1(),
		func2(),
		func3(),
	)
	print("Main Ended..")


asyncio.run(main())

