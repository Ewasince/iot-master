import aiohttp


async def perform_request(url) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return resp.ok
    except Exception as e:
        print(e)
        return False
