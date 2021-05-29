import numpy as np
import aiohttp
import aiofiles
import asyncio


API = "pk.eyJ1Ijoiam9oYW5yaCIsImEiOiJja29lbmQ2NDgwZTJqMm9xcDZqbzJ4Z3VnIn0.6iYEscod0GHS9V7h_9uThQ"

async def writeToFile(fn,x,y):
    async with aiohttp.ClientSession() as session:
        url = 'https://api.mapbox.com/v4/mapbox.satellite/{}/{}/{}@2x.pngraw?access_token=pk.eyJ1Ijoiam9oYW5yaCIsImEiOiJja29lbmQ2NDgwZTJqMm9xcDZqbzJ4Z3VnIn0.6iYEscod0GHS9V7h_9uThQ'.format(z,x,y)
        async with session.get(url) as res: 
            if res.status == 200:
                f = await aiofiles.open('./img/'+fn, mode='wb')
                await f.write(await res.read())
                await f.close() 

    
from tqdm import tqdm
async def fetch_all(data):
    i = 750000-625
    for x,y in tqdm(data):
            await writeToFile('{}.{}.png'.format(x,y),x,y)
            await asyncio.sleep(10)
            i -= 1
            if i <= 0:
                print(f"last request done, {x},{y}")
                break




if __name__ == '__main__' :
    asyncio.run(fetch_all())

