from aiohttp import web
import sys
sys.path.append('../../')
from App.utils.LogRecordManager import LogRecordManager


class PutHandler:
    @staticmethod
    def execute(routes,config):
        @routes.put('/{tail:.*}')
        async def get_handler(request):
            data = await request.content.read()
            LogRecordManager.record(data, "MyServer")
            putData = f"Successful, Put request rec:'{data.decode()}'(by:Server) "
            response = web.StreamResponse()
            if config.get('ServerSettings').get('EnableCustomHeader') is True:
                for key,val in config.get('ServerSettings').get('CustomHeaders'):
                    response.headers.add(key,val)
            response.content_type = "text/tab-separated-values; charset=utf-8"
            if config.get('ServerSettings').get('EnableCustomData') is True:
                putData = config.get('ServerSettings').get('CustomData')

            await response.prepare(request)
            await response.write(putData.encode("utf-8"))
            return response
