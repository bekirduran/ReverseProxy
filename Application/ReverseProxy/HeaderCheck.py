import toml
from aiohttp import web


class HeaderCheck:
    @staticmethod
    async def request(header):
        config = toml.load('../config.toml')
        check = False
        for item in config.get('filters').get('requestHeaderCheck'):
            if item[0] in header and item[1] == header[item[0]]:
                check = True
        return check

    @staticmethod
    async def response(header):
        config = toml.load('../config.toml')
        check = False
        for item in config.get('filters').get('responseHeaderCheck'):
            if item[0] in header and item[1] == header[item[0]]:
                check = True
        return check
