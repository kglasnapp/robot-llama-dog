import asyncio
import sys
import time

async def func1():
  print("Function 1 started..")
  await asyncio.sleep(2)
  print("Function 1 Ended")


async def func2():
    count = 0
    start = time.perf_counter()
    while True:
      print("Function 2 started..", time.perf_counter() - start)
      await asyncio.sleep(1)
      count += 1
      if count > 10:
          break
  


async def ainput(string: str) -> str:
    await asyncio.to_thread(sys.stdout.write, f'(string) ')
    return await asyncio.to_thread(sys.stdin.readline)

# Example usage:

async def func3():
    user_input = await ainput('Enter something: ')
    print(f'You entered: {user_input}')
    
async def main():
  await asyncio.gather(
    func1(),
    func2(),
    func3(),
  )
  print("Main Ended..")


asyncio.run(main())


