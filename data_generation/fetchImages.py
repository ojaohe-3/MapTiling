import numpy as np
import aiohttp
import aiofiles
import asyncio


API = "pk.eyJ1Ijoiam9oYW5yaCIsImEiOiJja29lbmQ2NDgwZTJqMm9xcDZqbzJ4Z3VnIn0.6iYEscod0GHS9V7h_9uThQ"

async def writeToFile(fn,x,y, session):
    url = f'https://api.mapbox.com/v4/mapbox.satellite/15/{x}/{y}@2x.pngraw?access_token={API}'
    async with session.get(url) as res: 
        if res.status == 200:
            f = await aiofiles.open(fn, mode='wb')
            await f.write(await res.read())
            await f.close()
            return 1
        elif res.status != 200 :
            print(x,y, "failed to load! reason:", res.status)
            return -1

    
from tqdm import tqdm
async def fetch_all(data, session):
    i = 10000
    for _ in tqdm(range(i)):
            x,y = data[int(np.random.uniform()*len(data))]
            status = await writeToFile('./img/{}.{}.png'.format(x,y),x,y, session)
            i -= 1
            if i <= 0 or status == -1:
                print(f"last request done, {x},{y}")
                return x, y


from poly import generate_polygon, get_polyfill
import concurrent.futures
from threading import Thread

async def execution_functor(data, executor):
    n = int(len(data)/12)
    regions = [data[i:i + n] for i in range(0, len(data), n)]
    loop = asyncio.get_event_loop() 
    tasks = [
        loop.run_in_executor(executor, fetch_all, regions[i])
        for i in range(12)
    ]
    await asyncio.wait(tasks)


def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def fetch_single(x,y,prefix):
    async with aiohttp.ClientSession() as session:
        status = await writeToFile(f'{prefix}/{x}.{y}.png',x,y, session)

async def fetch_all_session(data, loop):
    async with aiohttp.ClientSession() as session:
        n = int(len(data)/24)
        regions = [data[i:i + n] for i in range(0, len(data), n)]
        tasks = [loop.create_task(fetch_all(regions[i], session)) for i in range(24)]
        _ = await asyncio.gather(*tasks)

if __name__ == '__main__' :
    data = generate_polygon()
    data = get_polyfill(data[-1])
    loop = asyncio.new_event_loop()
    t = Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()

    task = asyncio.run_coroutine_threadsafe(fetch_all_session(data, loop), loop)
    print(task.result())