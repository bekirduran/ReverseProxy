from App.Util.RegexManager import RegexManager
from App.Util.LogRecordManager import LogRecordManager


class BodyReplacer:

    @staticmethod
    async def execute(bodyEncoded, config, isRequest):

        bodyReplacerOnOff = config.get('replacer').get('bodyReplacer')
        if not bodyReplacerOnOff:
            return bodyEncoded

        body = bodyEncoded.decode()
        if isRequest:
            for item in config.get('replacer').get('requestBody'):
                if item[0] in body:
                    newBodyContent = body.replace(item[0], item[1])
                    body = newBodyContent
                    LogRecordManager.record('Request body replaced: ' + item[0] + ' -> ' + item[1], 'reverseProxy')

            for item in config.get('replacer').get('requestBodyCaseInsensitive'):
                bodyContent = body
                if item[0].casefold() in bodyContent.casefold():
                    newBodyContent = bodyContent.casefold().replace(item[0], item[1])
                    body = newBodyContent
                    LogRecordManager.record('Request body case sensitive replaced: ' + item[0] + ' -> ' + item[1], 'reverseProxy')

            for key, val in config.get('replacer').get('requestBodyRegex'):
                bodyContent = body
                newBodyContent = RegexManager.replace(bodyContent, [key], val)
                if newBodyContent != bodyContent:
                    body = newBodyContent
                    LogRecordManager.record('Request body regex replaced: ' + key + ' -> ' + val, 'reverseProxy')
            return body.encode('utf-8')

        else:
            for item in config.get('replacer').get('responseBody'):
                bodyContent = body
                if item[0] in bodyContent:
                    newBodyContent = bodyContent.replace(item[0], item[1])
                    body = newBodyContent
                    LogRecordManager.record('Response body replaced: ' + item[0] + ' -> ' + item[1], 'reverseProxy')

            for key, val in config.get('replacer').get('responseBodyCaseInsensitive'):
                bodyContent = body
                if key.lower() in bodyContent.lower():
                    newBodyContent = bodyContent.lower().replace(key, val)
                    body = newBodyContent
                    LogRecordManager.record('Request body replaced: ' + key + ' -> ' + val, 'reverseProxy')

            for key, val in config.get('replacer').get('responseBodyRegex'):
                bodyContent = body
                newBodyContent = RegexManager.replace(bodyContent, [key], val)
                if newBodyContent != bodyContent:
                    body = newBodyContent
                    LogRecordManager.record('Response body regex replaced: ' + key + ' -> ' + val, 'reverseProxy')
            return body


class HeaderReplacer:

    @staticmethod
    async def execute(headers, config, isRequest):
        headerReplacerOnOff = config.get('replacer').get('headerReplacer')
        if not headerReplacerOnOff:
            return headers
        if isRequest:
            for item in config.get('replacer').get('requestHeader'):
                if item[0] in headers:
                    newHeader = headers.copy()
                    newHeader.add(item[1], newHeader.pop(item[0]))
                    headers = newHeader
                    LogRecordManager.record('Request header replaced: ' + item[0] + ' -> ' + item[1],'reverseProxy')
            return headers
        else:
            for item in config.get('replacer').get('responseHeader'):
                if item[0] in headers:
                    headers.add(item[1], headers.pop(item[0]))
                    LogRecordManager.record('Response header replaced: ' + item[0] + ' -> ' + item[1] ,'reverseProxy')
            return headers


class QueryPathReplacer:

    @staticmethod
    async def execute(request, config):
        requestQuery = request.query
        requestPath = request.path
        pathAndQueryReplacerOnOff = config.get('replacer').get('pathAndQueryReplacer')
        if not pathAndQueryReplacerOnOff:
            return requestQuery, requestPath

        for item in config.get('replacer').get('QueryReplacer'):
            if item[0] in request.query:
                newQuery = request.query.copy()
                newQuery.add(item[1], newQuery.pop(item[0]))
                requestQuery = newQuery
                LogRecordManager.record('Query path replaced: ' + item[0] + ' -> ' + item[1] ,'reverseProxy')
        for item in config.get('replacer').get('PathReplacer'):
            if item[0] == requestPath:
                requestPath = item[1]
                LogRecordManager.record('Path replaced: ' + item[0] + ' -> ' + item[1],'reverseProxy')
        return requestQuery, requestPath
