from aiohttp import web

from App.ReverseProxy.LogRecordManager import LogRecordManager


class PostHandler:
    @staticmethod
    def execute(routes,config):
        @routes.post('/{tail:.*}')
        async def get_handler(request):
            data = await request.content.read()
            LogRecordManager.record(data, "MyServer")
            postData = f"Successful, Post request received post data is:'{data.decode()}' (by:Server) "
            response = web.StreamResponse()
            if config.get('ServerSettings').get('EnableCustomHeader') is True:
                for key,val in config.get('ServerSettings').get('CustomHeaders'):
                    response.headers.add(key,val)
            response.content_type = "text/tab-separated-values; charset=utf-8"
            if config.get('ServerSettings').get('EnableCustomData') is True:
                postData = config.get('ServerSettings').get('CustomData')
            await response.prepare(request)
            await response.write(postData.encode("utf-8"))
            return response