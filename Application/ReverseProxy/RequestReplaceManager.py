import toml

from Application.ReverseProxy.RegexManager import RegexManager


class RequestReplaceManager:

    @staticmethod
    async def execute(request, requestBody, requestHeader, requestPath, requestQuery):
        config = toml.load('../config.toml')
        for item in config.get('replacer').get('requestBody'):
            bodyContent = requestBody.decode()
            if item[0] in bodyContent:
                newBodyContent = bodyContent.replace(item[0], item[1])
                requestBody = newBodyContent.encode('utf-8')
        for item in config.get('replacer').get('requestBodyCaseSensitive'):
            bodyContent = requestBody.decode()
            if item[0].casefold() in bodyContent.casefold():
                newBodyContent = bodyContent.casefold().replace(item[0], item[1])
                requestBody = newBodyContent.encode('utf-8')

        for key, val in config.get('replacer').get('requestBodyRegex'):
            bodyContent = requestBody.decode()
            newBodyContent = RegexManager.replace(bodyContent, [key], val)
            requestBody = newBodyContent.encode('utf-8')


        for item in config.get('replacer').get('requestHeader'):
            if (item[0]) in request.headers:
                newHeader = request.headers.copy()
                newHeader.add(item[1], newHeader.pop(item[0]))
                requestHeader = newHeader
        for item in config.get('replacer').get('QueryReplacer'):
            if item[0] in request.query:
                newQuery = request.query.copy()
                newQuery.add(item[1], newQuery.pop(item[0]))
                requestQuery = newQuery
        for item in config.get('replacer').get('PathReplacer'):
            if item[0] == requestPath:
                requestPath = item[1]

        return requestBody, requestHeader, requestPath, requestQuery