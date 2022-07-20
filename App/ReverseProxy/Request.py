import aiohttp


class Request:
    @staticmethod
    async def execute(method, url, data, header, query):
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=data, headers=header, params=query) as resp:
                return await resp.read(), resp.headers, resp.status

