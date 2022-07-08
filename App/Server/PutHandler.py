from aiohttp import web

from App.Util.LogRecordManager import LogRecordManager


class PutHandler:
    @staticmethod
    def execute(routes):
        @routes.put('/{tail:.*}')
        async def get_handler(request):
            data = await request.content.read()
            LogRecordManager.record(data, "MyServer")
            putData = f"Successful, Put request rec:'{data.decode()}'(by:Server) "
            response = web.StreamResponse()
            response.content_type = "text/tab-separated-values; charset=utf-8"
            response.headers.add("TokenId", "12345")
            await response.prepare(request)
            await response.write(putData.encode("utf-8"))
            return response
