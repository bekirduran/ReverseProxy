import argparse
import ssl
import aiohttp
from aiohttp import web
import toml

from Application.ReverseProxy.HeaderCheck import HeaderCheck
from Application.ReverseProxy.RequestFilterManager import RequestFilterManager
from Application.ReverseProxy.RequestReplaceManager import RequestReplaceManager
from Application.ReverseProxy.ResponseFilterManager import ResponseFilterManager
from Application.ReverseProxy.ResponseReplaceManager import ResponseReplaceManager
from Application.ReverseProxy.Request import Request

parser = argparse.ArgumentParser(description='ProxyServer Argument Parser:::::')
parser.add_argument('--path')
parser.add_argument('--port')
args = parser.parse_args()
config = toml.load('../config.toml')
routes = web.RouteTableDef()


@routes.route("*", "/{tail:.*}")
async def all_handler(request):
    print(
        f"Request Accepted(Reverse Server)::::::\nMethod :{request.method}, request ip: {request.remote},")
    requestBody = await request.content.read()
    requestHeader = request.headers
    requestQuery = request.query
    requestPath = request.path

    """ --- Request body and header filter ---"""
    block, response = await RequestFilterManager.execute(request, requestBody)
    if block is True:
        return response
    """ --- Request header check ---"""
    if not await HeaderCheck.request(requestHeader):
        return web.Response(text=config.get('errorResponses').get('reqHeaderCheckError'))

    """ --- Request body and header replacer ---"""
    requestBody, requestHeader, requestPath, requestQuery = await RequestReplaceManager.execute(request, requestBody, requestHeader,requestPath, requestQuery)

    """ --- Http Operations ---"""
    serverUrl: str = config.get('url').get('localServerSSLUrl') if config.get('ssl').get('enable') else config.get('url').get('localServerUrl')
    serverUrl = serverUrl + requestPath
    try:
        if request.method == "PUT":
            response = await Request.execute(request.method, serverUrl, requestBody, requestHeader, requestQuery)
        elif request.method == "POST":
            response = await Request.execute(request.method, serverUrl, requestBody, requestHeader, requestQuery)
        elif request.method == "GET":
            response = await Request.execute(request.method, serverUrl, "", requestHeader, requestQuery)
    except aiohttp.ClientSSLError as e:
        print("Client SSL Error: ", e)
        assert isinstance(e, ssl.SSLError)

    """ ----Response body and header filter---"""
    block, filterResponse = await ResponseFilterManager.execute(response)
    if block is True:
        return filterResponse
    """ --- Response header check ---"""
    if not await HeaderCheck.response(response.headers):
        return web.Response(text=config.get('errorResponses').get('resHeaderCheckError'))

    """ ----Response body and header replacer---"""
    response = await ResponseReplaceManager.execute(response)
    return response

app = web.Application()
app.add_routes(routes)

if config.get('ssl').get('enable') is True:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.get('ssl').get('cert'), config.get('ssl').get('key'))
    web.run_app(app, path=args.path, port=args.port,ssl_context=ssl_context)
else:
    web.run_app(app, path=args.path, port=args.port)

