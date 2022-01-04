import asyncio

async def counter(name: str):
    for i in range(0, 10):
        print(f"{name}: {i!s}")
        await asyncio.sleep(0)

# The event loop has 5 tasks: main, and the 4 "counter" coroutines added to the event loop as tasks
# coroutines
# futures
## awaiting a future does one of three things
## If the process the future represents has finished and returned a value then the await statement immediately returns that value.
## If the process the future represents has finished and raised an exception then the await statement immediately raises that exception.
## If the process the future represents has not yet finished then the current Task is paused until the process has finished. Once it is finished it behaves as described in the first two bullet points here.
# tasks (inherits from futures)
async def main():
    tasks = []
    for n in range(0, 4):
        tasks.append(asyncio.get_event_loop().create_task(counter(f"task{n}")))

    while True:
        print('Start')
        tasks = [t for t in tasks if not t.done()]
        if len(tasks) == 0:
            return

        print('Main')
        await asyncio.sleep(0)

loop = asyncio.get_event_loop()
try:
  loop.run_until_complete(main())
finally:
  loop.close()