import toml
from aiohttp import web

from Application.ReverseProxy.RegexManager import RegexManager


class RequestFilterManager:

    @staticmethod
    async def execute(request, body):
        config = toml.load('../config.toml')

        requestBody = body
        requestHeader = request.headers
        response = web.Response()

        if True in list(map(lambda method: True if method == request.method else False,
                            config.get('filters').get('InvalidMethods'))):
            return True, web.Response(text=config.get('errorResponses').get('invalidMethodError'))
        if True in list(map(lambda path: True if path in request.path else False,
                            config.get('filters').get('InvalidPathValues'))):
            return True, web.Response(text=config.get('errorResponses').get('invalidPathError'))
        if True in list(map(lambda query: True if query in request.query else False,
                            config.get('filters').get('InvalidQueryValues'))):
            return True, web.Response(text=config.get('errorResponses').get('invalidQueryError'))
        if True in list(map(lambda word: True if word in requestHeader else False,
                            config.get('filters').get('requestHeaders'))):
            return True, web.Response(text=config.get('errorResponses').get('headerReqError'))
        if True in list(map(lambda word: True if word in requestBody.decode() else False,
                            config.get('filters').get('requestBody'))):
            return True, web.Response(text=config.get('errorResponses').get('requestFilter'))
        if True in list(map(lambda word: True if word.lower() in requestBody.decode().lower() else False,
                            config.get('filters').get('requestBodyCaseSensitive'))):
            return True, web.Response(text=config.get('errorResponses').get('requestFilter')+' (case sensitive)')
        if RegexManager.execute(requestBody.decode(), config.get('filters').get('requestBodyRegex')):
            return True, web.Response(text=config.get('errorResponses').get('reqRegexError'))
        return False, response
