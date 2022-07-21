from aiohttp import web


import LogRecordManager
import RegexManager


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
            filterBodyText = config.get('filters').get('requestBody')
            errorResponseText = config.get('errorResponses').get('requestFilter')
            filterBodyTextCaseInsensitive = config.get('filters').get('requestBodyCaseInsensitive')
            filterRegexBodyText = config.get('filters').get('requestBodyRegex')
            errorResponseRegexText = config.get('errorResponses').get('reqRegexError')
        else:
            filterBodyText = config.get('filters').get('responseBody')
            errorResponseText = config.get('errorResponses').get('responseFilter')
            filterBodyTextCaseInsensitive = config.get('filters').get('responseBodyCaseInsensitive')
            filterRegexBodyText = config.get('filters').get('responseBodyRegex')
            errorResponseRegexText = config.get('errorResponses').get('resRegexError')

        if True in list(map(lambda word: True if word in body else False, filterBodyText)):
            flag = True
            bodyText += errorResponseText + '\n'
            LogRecordManager.record(errorResponseText, 'reverseProxy')
        if True in list(map(lambda word: True if word.lower() in body.lower() else False, filterBodyTextCaseInsensitive)):
            flag = True
            bodyText += errorResponseText + ' (case insensitive)' + '\n'
            LogRecordManager.record(errorResponseText + ' (case insensitive)', 'reverseProxy')
        if RegexManager.execute(body, filterRegexBodyText):
            flag = True
            bodyText += errorResponseRegexText + '\n'
            LogRecordManager.record(errorResponseRegexText, 'reverseProxy')
        bodyFilterResponse.text = bodyText
        bodyFilterResponse.set_status(404)
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
            headerText = config.get('filters').get('requestHeaders')
            errorResponse = config.get('errorResponses').get('headerReqError')
            checkerResponse = config.get('errorResponses').get('reqHeaderCheckError')
        else:
            headerText = config.get('filters').get('responseHeaders')
            errorResponse = config.get('errorResponses').get('headerResError')
            checkerResponse = config.get('errorResponses').get('resHeaderCheckError')

        if True in list(map(lambda word: True if word in header else False, headerText)):
            flag = True
            bodyText += errorResponse + '\n'
            LogRecordManager.record(errorResponse, 'reverseProxy')
        if not await HeaderCheck.request(header, config):
            flag = True
            bodyText += checkerResponse + '\n'
            LogRecordManager.record(checkerResponse, 'reverseProxy')
        headerFilterResponse.text = bodyText
        headerFilterResponse.set_status(403)
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
