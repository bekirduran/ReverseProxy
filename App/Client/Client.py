import argparse
import asyncio

import aiohttp
import toml
from App.utils.LogRecordManager import LogRecordManager


class Client:
    targetUrl: str

    def __init__(self, url):
        self.targetUrl = url

    async def makeRequest(self, method, body, header):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.request(method, "http://"+self.targetUrl, data=body, headers=header,ssl=False) as resp:
                LogRecordManager.record(f"Client method: {method} - proxy status: {resp.status} - proxy response: {await resp.text()}", "Client")
                response = await resp.text()
                return response

    async def run(self, number, method, data, header):
        tasks = []
        for i in range(number):
            task = asyncio.ensure_future(self.makeRequest(method, data, header))
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        print(responses)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client Argument Parser:::::')
    parser.add_argument('--toml', type=str, help='toml file path', default='../client.toml')
    args = parser.parse_args()
    config = toml.load(args.toml)
    client = Client(config.get('ClientSettings').get('URI'))

    data = "test key1"
    header = {'apiKey': '1071', 'TokenId':'12345'}
    method = config.get('ClientSettings').get('RequestMethod')

    if config.get('ClientSettings').get('EnableCustomHeader') is True:
        header = config.get('ClientSettings').get('CustomHeaders')
    if config.get('ClientSettings').get('EnableCustomData') is True:
        data = config.get('ClientSettings').get('CustomData')

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(client.run(200, method, data, header))
    loop.run_until_complete(future)

