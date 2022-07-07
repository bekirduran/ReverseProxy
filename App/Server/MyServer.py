import argparse
import ssl
import toml
from aiohttp import web

from App.Util.LogRecordManager import LogRecordManager

parser = argparse.ArgumentParser(description="aiohttp server example")
args = parser.parse_args()
parser.add_argument('--ip')
config = toml.load('../config.toml')

app = web.Application()
routes = web.RouteTableDef()


@routes.get('/{tail:.*}')
async def get_handler(request):
    data = "Successful, Get request received to client (by:Server)"
    LogRecordManager.record(data,"MyServer")
    response = web.StreamResponse()
    response.content_type = "text/tab-separated-values; charset=utf-8"
    response.headers.add("TokenId", "12345")
    await response.prepare(request)
    await response.write(data.encode("utf-8"))
    return response


@routes.post('/{tail:.*}')
async def post_handler(request):
    data = await request.content.read()
    LogRecordManager.record(data,"MyServer")
    postData = f"Successful, Post request received post data is:'{data.decode()}' (by:Server) "
    response = web.StreamResponse()
    response.content_type = "text/tab-separated-values; charset=utf-8"
    response.headers.add("TokenId", "12345")
    await response.prepare(request)
    await response.write(postData.encode("utf-8"))
    return response


@routes.put('/{tail:.*}')
async def put_handler(request):
    data = await request.content.read()
    LogRecordManager.record(data,"MyServer")
    putData = f"Successful, Put request rec:'{data.decode()}'(by:Server) "
    response = web.StreamResponse()
    response.content_type = "text/tab-separated-values; charset=utf-8"
    response.headers.add("TokenId", "12345")
    await response.prepare(request)
    await response.write(putData.encode("utf-8"))
    return response

app.add_routes(routes)
args.ip = '192.168.30.7'
if config.get('ssl').get('enable') is True:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.get('ssl').get('cert'), config.get('ssl').get('key'))
    web.run_app(app, host=args.ip, ssl_context=ssl_context)
else:
    web.run_app(app, host=args.ip)