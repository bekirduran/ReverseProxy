import aiohttp
import toml
import ssl


class Request:
    @staticmethod
    async def execute(method, url, data, header, query):
        config = toml.load('../config.toml')

        #ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        #ssl_context.load_cert_chain(config.get('ssl').get('cert'), config.get('ssl').get('key'))
        print("URL: ", url)
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=data, headers=header, params=query) as resp:
                return await resp.read(), resp.headers, resp.status

