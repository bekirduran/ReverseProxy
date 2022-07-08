from aiohttp import web
from App.Util.LogRecordManager import LogRecordManager


class DeleteHandler:

    @staticmethod
    def execute(routes):
        @routes.delete('/{tail:.*}')
        async def put_handler(request):
            data = await request.content.read()
            LogRecordManager.record(data, "MyServer")
            putData = f"Successful, Deleted data if exist:'{data.decode()}'(by:Server) "
            response = web.StreamResponse()
            response.content_type = "text/tab-separated-values; charset=utf-8"
            response.headers.add("TokenId", "12345")
            await response.prepare(request)
            await response.write(putData.encode("utf-8"))
            return response
