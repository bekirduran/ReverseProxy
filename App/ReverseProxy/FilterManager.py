from aiohttp import web

from App.Util.RegexManager import RegexManager
from App.Util.LogRecordManager import LogRecordManager


class BodyFilter:

    @staticmethod
    async def execute(bodyEncoded, config, isRequest):
        bodyFilterOnOff = config.get('filters').get('bodyFilter')
        if not bodyFilterOnOff:
            return False, bodyEncoded

        body = bodyEncoded.decode()
        bodyText = ""
        flag = False
        bodyFilterResponse = web.Response()
        if isRequest:
            if True in list(map(lambda word: True if word in body else False,
                                config.get('filters').get('requestBody'))):
                flag = True
                bodyText += config.get('errorResponses').get('requestFilter') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('requestFilter'), 'reverseProxy')
            if True in list(map(lambda word: True if word.lower() in body.lower() else False,
                                config.get('filters').get('requestBodyCaseInsensitive'))):
                flag = True
                bodyText += config.get('errorResponses').get('requestFilter') + ' (case insensitive)' + '\n'
                LogRecordManager.record(config.get('errorResponses').get('requestFilter') + ' (case insensitive)', 'reverseProxy')
            if RegexManager.execute(body, config.get('filters').get('requestBodyRegex')):
                flag = True
                bodyText += config.get('errorResponses').get('reqRegexError') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('reqRegexError'),'reverseProxy')
            bodyFilterResponse.text = bodyText
            bodyFilterResponse.set_status(404)
            return flag, bodyFilterResponse

        else:
            if True in list(
                    map(lambda header: True if header in body else False, config.get('filters').get('responseBody'))):
                flag = True
                bodyText += config.get('errorResponses').get('responseFilter') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('responseFilter'), 'reverseProxy')
            if True in list(map(lambda header: True if header.lower() in body.lower() else False,
                                config.get('filters').get('responseBodyCaseInsensitive'))):
                flag = True
                bodyText += config.get('errorResponses').get('responseFilter') + ' (case insensitive)' + '\n'
                LogRecordManager.record(config.get('errorResponses').get('responseFilter')+'(case insensitive)', 'reverseProxy')
            if RegexManager.execute(body, config.get('filters').get('responseBodyRegex')):
                flag = True
                bodyText += config.get('errorResponses').get('resRegexError') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('resRegexError'), 'reverseProxy')
            bodyFilterResponse.text = bodyText
            bodyFilterResponse.set_status(504)
            return flag, bodyFilterResponse


class HeaderFilter:

    @staticmethod
    async def execute(header, config, isRequest):
        headerFilterOnOff = config.get('filters').get('headerFilter')
        if not headerFilterOnOff:
            return False, header

        bodyText = ""
        flag = False
        headerFilterResponse = web.Response()
        if isRequest:
            if True in list(map(lambda word: True if word in header else False,
                                config.get('filters').get('requestHeaders'))):
                flag = True
                bodyText += config.get('errorResponses').get('headerReqError') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('headerReqError'), 'reverseProxy')
            if not await HeaderCheck.request(header, config):
                flag = True
                bodyText += config.get('errorResponses').get('reqHeaderCheckError') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('reqHeaderCheckError'), 'reverseProxy')
            headerFilterResponse.text = bodyText
            headerFilterResponse.set_status(403)
            return flag, headerFilterResponse
        else:
            if True in list(
                    map(lambda word: True if word in header else False, config.get('filters').get('responseHeaders'))):
                flag = True
                bodyText += config.get('errorResponses').get('headerResError') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('headerResError'), 'reverseProxy')
            if not await HeaderCheck.response(header, config):
                flag = True
                bodyText += config.get('errorResponses').get('resHeaderCheckError') + '\n'
                LogRecordManager.record(config.get('errorResponses').get('resHeaderCheckError'), 'reverseProxy')
            headerFilterResponse.text = bodyText
            headerFilterResponse.set_status(501)
            return flag, headerFilterResponse


class QueryPathFilter:

    @staticmethod
    async def execute(request, config):
        queryPathFilterOnOff = config.get('filters').get('pathAndQueryFilter')
        if not queryPathFilterOnOff:
            return False, request
        bodyText = ""
        flag = False
        queryPathFilterResponse = web.Response()

        if True in list(map(lambda word: True if word in request.query else False,
                            config.get('filters').get('InvalidQueryValues'))):
            flag = True
            bodyText += config.get('errorResponses').get('invalidQueryError') + '\n'
            LogRecordManager.record(config.get('errorResponses').get('invalidQueryError'), 'reverseProxy')
        queryPathFilterResponse.text = bodyText
        queryPathFilterResponse.set_status(402)

        if True in list(map(lambda path: True if path in request.path else False,
                            config.get('filters').get('InvalidPathValues'))):
            flag = True
            bodyText += config.get('errorResponses').get('invalidPathError') + '\n'
            LogRecordManager.record(config.get('errorResponses').get('invalidPathError'), 'reverseProxy')
        queryPathFilterResponse.text = bodyText
        queryPathFilterResponse.set_status(402)
        return flag, queryPathFilterResponse


class MethodFilter:

    @staticmethod
    async def execute(request, config):
        methodFilterOnOff = config.get('filters').get('methodFilter')
        if not methodFilterOnOff:
            return False, request
        bodyText = ""
        flag = False
        methodFilterResponse = web.Response()
        if request.method not in config.get('filters').get('validMethods'):
            flag = True
            bodyText += config.get('errorResponses').get('invalidMethodError')
            LogRecordManager.record(config.get('errorResponses').get('invalidMethodError'), 'reverseProxy')
        methodFilterResponse.text = bodyText
        methodFilterResponse.set_status(401)
        return flag, methodFilterResponse


class HeaderCheck:
    @staticmethod
    async def request(header,config):
        check = False
        for item in config.get('filters').get('requestHeaderCheck'):
            if item[0].casefold() in header and item[1].casefold() == header[item[0]].casefold():
                check = True
        return check

    @staticmethod
    async def response(header,config):
        check = False
        for item in config.get('filters').get('responseHeaderCheck'):
            if item[0].casefold() in header and item[1].casefold() == header[item[0]].casefold():
                check = True
        return check
