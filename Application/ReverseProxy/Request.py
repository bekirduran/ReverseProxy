import aiohttp
import toml
import ssl
from aiohttp import web


class Request:
    @staticmethod
    async def execute(method, url, data, header, query):
        config = toml.load('../config.toml')
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(config.get('ssl').get('cert'), config.get('ssl').get('key'))
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, data=data, headers=header, params=query,
                                       ssl=ssl_context if config.get('ssl').get('enable') else False) as resp:
                response = web.Response()
                response.text = await resp.text()
                response.headers.add("header1", "val-header")
                response.headers.add("TokenId", "12345")
                return response
