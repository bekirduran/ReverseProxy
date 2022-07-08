from aiohttp import web
from App.Util.LogRecordManager import LogRecordManager


class GetHandler:

    @staticmethod
    def execute(routes):
        @routes.get('/{tail:.*}')
        async def get_handler(request):
            data = "Successful, Get request received to client (by:Server)"
            LogRecordManager.record(data, "MyServer")
            response = web.StreamResponse()
            response.content_type = "text/tab-separated-values; charset=utf-8"
            response.headers.add("TokenId", "12345")
            await response.prepare(request)
            await response.write(data.encode("utf-8"))
            return response
