from aiohttp import web

from App.Util.LogRecordManager import LogRecordManager


class PostHandler:
    @staticmethod
    def execute(routes):
        @routes.post('/{tail:.*}')
        async def get_handler(request):
            data = await request.content.read()
            LogRecordManager.record(data, "MyServer")
            postData = f"Successful, Post request received post data is:'{data.decode()}' (by:Server) "
            response = web.StreamResponse()
            response.content_type = "text/tab-separated-values; charset=utf-8"
            response.headers.add("TokenId", "12345")
            await response.prepare(request)
            await response.write(postData.encode("utf-8"))
            return response