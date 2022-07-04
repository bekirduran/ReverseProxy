import argparse
import ssl
import toml
from aiohttp import web

parser = argparse.ArgumentParser(description="aiohttp server example")
parser.add_argument('--path')
parser.add_argument('--port')
args = parser.parse_args()

config = toml.load('../config.toml')

app = web.Application()
routes = web.RouteTableDef()


@routes.get('/{tail:.*}')
async def get_handler(request):
    print(f"Received : server get")
    print(request.headers)
    print(request.url)
    print(request.query)
    data = "Successful, Get request received to client (by:Server)"
    response = web.Response()
    response.text = data
    return response


@routes.post('/{tail:.*}')
async def post_handler(request):
    print(f"Received : server post")
    print(request.headers)
    print(request.url)
    print(request.query)
    data = await request.content.read()
    postData = f"Successful, Post request received post data is:'{data.decode()}' (by:Server) "
    response = web.Response()
    response.text = postData
    return response


@routes.put('/{tail:.*}')
async def put_handler(request):
    print(f"Received : server put")
    print(request.headers)
    print(request.url)
    print(request.query)
    data = await request.content.read()
    putData = f"Successful, Put request rec:'{data.decode()}'(by:Server) "
    response = web.Response()
    response.text = putData
    return response

app.add_routes(routes)

if config.get('ssl').get('enable') is True:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.get('ssl').get('cert'), config.get('ssl').get('key'))
    args.port = 6843
    web.run_app(app, path=args.path, port=args.port, ssl_context=ssl_context)
else:
    args.port = 6868
    web.run_app(app, path=args.path, port=args.port)