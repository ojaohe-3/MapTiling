import numpy as np
import aiohttp
import aiofiles
import asyncio
from poly import generate_polygon, get_polyfill
from threading import Thread
from tqdm import tqdm

def get_api():
    if os.path.isfile('./api'):
        with open('./api', 'r') as f:
            api = f.readline()
        return api
    else:
        return None

async def writeToFile(fn,x,y, session):
    API = get_api()
    if API:
        url = f'https://api.mapbox.com/v4/mapbox.satellite/15/{x}/{y}@1x.png32?access_token={API}'
        async with session.get(url) as res: 
            if res.status == 200:
                f = await aiofiles.open(fn, mode='wb')
                await f.write(await res.read())
                await f.close()
                return 1
            elif res.status != 200 :
                print(x,y, "failed to load! reason:", res.status)
                return -1
    else:
        return -1
    
async def fetch_all(data, file_path, session):
    for d in tqdm(data):
            x,y = d
            status = await writeToFile('{}/{}.{}.png'.format(file_path, x,y),x,y, session)
            if status == -1:
                print(f"last request done, {x},{y}")
                break
    return x, y


async def fetch_single(x,y,prefix):
    async with aiohttp.ClientSession() as session:
        await writeToFile(f'{prefix}/{x}.{y}.png',x,y, session)

async def fetch_all_session(data,n, file_path, loop):
    async with aiohttp.ClientSession() as session:
        regions = [data[i:i + n] for i in range(0, len(data), n)]
        tasks = [loop.create_task(fetch_all(regions[i], file_path, session)) for i in range(24)]
        _ = await asyncio.gather(*tasks)



def start_background_loop(loop: asyncio.AbstractEventLoop) -> None:
    asyncio.set_event_loop(loop)
    loop.run_forever()

def run_multi_fetch(data, n, file_path):
    loop = asyncio.new_event_loop()
    t = Thread(target=start_background_loop, args=(loop,), daemon=True)
    t.start()
    task = asyncio.run_coroutine_threadsafe(fetch_all_session(data,n, file_path, loop), loop)
    task.result()

import os
if __name__ == '__main__' :
    # data = generate_polygon()
    data = [p.split('.')[:-1] for p in os.listdir('./data/train/') ]
    data = np.array([np.array([x,y]) for x,y in data])
    # data = get_polyfill(data[-1])
    run_multi_fetch(data, int(len(data)/24), './data/train/')