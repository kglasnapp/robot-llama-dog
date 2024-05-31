#!/usr/bin/env python3
# countasync.py

import asyncio
import time

async def count(a):
    print("One",a)
    await asyncio.sleep(10)
    print("Two",a)

async def main():
    asyncio.gather(count(1), count(2), count(3))

async def io():
  while True:
    print("Time:", time.perf_counter())
    await asyncio.sleep(5)
 
 
async def main():
    s = time.perf_counter()
    print(1)
    task = asyncio.create_task(io())
    print(2)
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

asyncio.run(main())
