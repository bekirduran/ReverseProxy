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
            replacingText = config.get('replacer').get('requestBody')
            logText = 'Request body replaced: '
            replacingInsensitiveText = config.get('replacer').get('requestBodyCaseInsensitive')
            replacingRegexText = config.get('replacer').get('requestBodyRegex')
            logRegexText = 'Request body regex replaced: '
        else:
            replacingText = config.get('replacer').get('responseBody')
            logText = 'Response body replaced: '
            replacingInsensitiveText = config.get('replacer').get('responseBodyCaseInsensitive')
            replacingRegexText = config.get('replacer').get('responseBodyRegex')
            logRegexText = 'Response body regex replaced: '

        for item in replacingText:
            if item[0] in body:
                newBodyContent = body.replace(item[0], item[1])
                body = newBodyContent
                LogRecordManager.record(logText + item[0] + ' -> ' + item[1], 'reverseProxy')
        for item in replacingInsensitiveText:
            bodyContent = body
            if item[0].casefold() in bodyContent.casefold():
                newBodyContent = bodyContent.casefold().replace(item[0], item[1])
                body = newBodyContent
                LogRecordManager.record(logText+ 'insensitive ' + item[0] + ' -> ' + item[1], 'reverseProxy')
        for key, val in replacingRegexText:
            bodyContent = body
            newBodyContent = RegexManager.replace(bodyContent, [key], val)
            if newBodyContent != bodyContent:
                body = newBodyContent
                LogRecordManager.record(logRegexText + key + ' -> ' + val, 'reverseProxy')
        return body.encode('utf-8') if isRequest else body


class HeaderReplacer:

    @staticmethod
    async def execute(headers, config, isRequest):
        headerReplacerOnOff = config.get('replacer').get('headerReplacer')
        if not headerReplacerOnOff:
            return headers

        if isRequest:
            replacingHeaderText = config.get('replacer').get('requestHeader')
            logText = 'Request header replaced: '
        else:
            replacingHeaderText = config.get('replacer').get('responseHeader')
            logText = 'Response header replaced: '

        if isRequest:
            for item in replacingHeaderText:
                if item[0] in headers:
                    newHeader = headers.copy()
                    newHeader.add(item[1], newHeader.pop(item[0]))
                    headers = newHeader
                    LogRecordManager.record(logText + item[0] + ' -> ' + item[1], 'reverseProxy')
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
