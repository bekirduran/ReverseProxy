import toml
from aiohttp import web

from Application.ReverseProxy.RegexManager import RegexManager


class ResponseFilterManager:
    @staticmethod
    async def execute(response):
        config = toml.load('../config.toml')
        responseBody = response.body.decode()
        responseHeader = response.headers
        if True in list(map(lambda header: True if header in responseBody else False, config.get('filters').get('responseBody'))):
            return True, web.Response(text=config.get('errorResponses').get('responseFilter'))
        if True in list(map(lambda header: True if header.lower() in responseBody.lower() else False, config.get('filters').get('responseBodyCaseSensitive'))):
            return True, web.Response(text=config.get('errorResponses').get('responseFilter')+' (case sensitive)')
        if True in list(map(lambda header: True if header in responseHeader else False, config.get('filters').get('responseHeaders'))):
            return True, web.Response(text=config.get('errorResponses').get('headerResError'))
        if RegexManager.execute(responseBody, config.get('filters').get('responseBodyRegex')):
            return True, web.Response(text=config.get('errorResponses').get('resRegexError'))
        return False, response