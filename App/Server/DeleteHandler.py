from aiohttp import web
from App.ReverseProxy.LogRecordManager import LogRecordManager


class DeleteHandler:

    @staticmethod
    def execute(routes,config):
        @routes.delete('/{tail:.*}')
        async def put_handler(request):
            data = await request.content.read()
            LogRecordManager.record(data, "MyServer")
            delData = f"Successful, Deleted data if exist:'{data.decode()}'(by:Server) "
            response = web.StreamResponse()
            if config.get('ServerSettings').get('EnableCustomHeader') is True:
                for key,val in config.get('ServerSettings').get('CustomHeaders'):
                    response.headers.add(key,val)
            response.content_type = "text/tab-separated-values; charset=utf-8"
            if config.get('ServerSettings').get('EnableCustomData') is True:
                delData = config.get('ServerSettings').get('CustomData')
            await response.prepare(request)
            await response.write(delData.encode("utf-8"))
            return response
