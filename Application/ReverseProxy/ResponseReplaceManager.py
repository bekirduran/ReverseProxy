import toml
from Application.ReverseProxy.RegexManager import RegexManager


class ResponseReplaceManager:

    @staticmethod
    async def execute(response):
        config = toml.load('../config.toml')
        for item in config.get('replacer').get('responseBody'):
            bodyContent = response.text
            if item[0] in bodyContent:
                newBodyContent = bodyContent.replace(item[0], item[1])
                response.text = newBodyContent

        for key, val in config.get('replacer').get('responseBodyCaseSensitive'):
            bodyContent = response.text
            if key.lower() in bodyContent.lower():
                newBodyContent = bodyContent.lower().replace(key, val)
                response.text = newBodyContent

        for key, val in config.get('replacer').get('responseBodyRegex'):
            bodyContent = response.text
            newBodyContent = RegexManager.replace(bodyContent, [key], val)
            response.text = newBodyContent

        for item in config.get('replacer').get('responseHeader'):
            if (item[0]) in response.headers:
                response.headers.add(item[1], response.headers.pop(item[0]))
        return response
