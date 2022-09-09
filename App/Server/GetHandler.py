from aiohttp import web
import sys
sys.path.append('../../')
from App.utils.LogRecordManager import LogRecordManager


class GetHandler:

    @staticmethod
    def execute(routes,config):
        @routes.get('/{tail:.*}')
        async def get_handler(request):
            print(request.headers)
            data = "Successful, Get request received to client (by:Server)"
            LogRecordManager.record(data, "MyServer")
            response = web.StreamResponse()
            if config.get('ServerSettings').get('EnableCustomHeader') is True:
                for key,val in config.get('ServerSettings').get('CustomHeaders'):
                    response.headers.add(key,val)
            response.content_type = "text/tab-separated-values; charset=utf-8"
            if config.get('ServerSettings').get('EnableCustomData') is True:
                data = config.get('ServerSettings').get('CustomData')

            await response.prepare(request)
            await response.write(data.encode("utf-8"))
            print(response.headers)

            return response
