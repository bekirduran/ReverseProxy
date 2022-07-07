import asyncio
import ssl

import aiohttp
import toml

config = toml.load('../config.toml')

proxyUrl = config.get('url').get('proxyServerSSLUrl') if config.get('ssl').get('enable') else config.get('url').get('proxyServerUrl')


class Client:
    targetUrl: str

    def __init__(self, url):
        self.targetUrl = url

    async def makeRequest(self, method, body, header):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.request(method, proxyUrl, data=body, headers=header,ssl=False) as resp:
                print(f"proxy status: {resp.status}")
                print(f"return message: {await resp.text()}")


if __name__ == '__main__':
    client = Client(proxyUrl)

    data = "test key1"
    header = {'apiKey': '1071', 'token':'1234'}
    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.makeRequest("PUT", data, header))
