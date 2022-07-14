import argparse
import asyncio

import aiohttp
import toml
from App.Util.LogRecordManager import LogRecordManager


class Client:
    targetUrl: str

    def __init__(self, url):
        self.targetUrl = url

    async def makeRequest(self, method, body, header):
        async with aiohttp.ClientSession(trust_env=True) as session:
            async with session.request(method, "https://"+self.targetUrl, data=body, headers=header,ssl=False) as resp:
                print(f"proxy status: {resp.status}")
                print(f"return message: {await resp.text()}")
                LogRecordManager.record(f"Client method: {method} - proxy status: {resp.status} - proxy response: {await resp.text()}", "Client")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Client Argument Parser:::::')
    parser.add_argument('--toml', type=str, help='toml file path', default='../client.toml')
    args = parser.parse_args()
    config = toml.load(args.toml)
    client = Client(config.get('ClientSettings').get('URI'))

    data = "test key1"
    header = {'apiKey': '1071', 'TokenId':'12345'}
    method = "GET"

    if config.get('ClientSettings').get('EnableCustomHeader') is True:
        header = config.get('ClientSettings').get('CustomHeaders')
    if config.get('ClientSettings').get('EnableCustomData') is True:
        data = config.get('ClientSettings').get('CustomData')

    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.makeRequest(method, data, header))
