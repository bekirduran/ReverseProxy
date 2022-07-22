import re


class RegexManager:

    @staticmethod
    def execute(string, regexList):
        result = False
        for eachRegex in regexList:
            if re.search(eachRegex, string):
                result = True
        return result

    @staticmethod
    def replace(body, regexList, newString):
        result = body
        for eachRegex in regexList:
            result = re.sub(eachRegex, newString, body)
        return result
