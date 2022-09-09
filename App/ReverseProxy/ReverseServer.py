import argparse
import ssl
from aiohttp import web
import toml
import sys

sys.path.append('../../')
from App.ReverseProxy import FilterManager, ReplaceManager
from App.ReverseProxy.Request import Request

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='ProxyServer Argument Parser:::::')
    parser.add_argument('-t','--toml', type=str, help='toml file path', default='../configs/config.toml')
    args = parser.parse_args()
    config = toml.load(args.toml)
    routes = web.RouteTableDef()


    @routes.route("*", "/{tail:.*}")
    async def all_handler(request):
        print("header: ", request.headers)

        block, methodResponse = await FilterManager.MethodFilter.execute(request, config)
        if block is True:
            return methodResponse

        block, headerResponse = await FilterManager.HeaderFilter.execute(request.headers, config, True)
        if block is True:
            return headerResponse

        block, queryPathResponse = await FilterManager.QueryPathFilter.execute(request, config)
        if block is True:
            return queryPathResponse

        requestBody = await request.content.read()
        block, bodyResponse = await FilterManager.BodyFilter.execute(requestBody, config, True)
        if block is True:
            return bodyResponse

        requestQuery, requestPath = await ReplaceManager.QueryPathReplacer.execute(request, config)
        requestHeader = await ReplaceManager.HeaderReplacer.execute(request.headers, config, True)
        requestBody = await ReplaceManager.BodyReplacer.execute(requestBody, config, True)

        serverUrl: str = config.get('url').get('Server_IP') if config.get('ssl').get('enable') else config.get(
            'url').get('Server_IP')
        serverUrl = serverUrl + requestPath

        respBody, respHeader, respStatus = await Request.execute(request.method, serverUrl, requestBody, requestHeader,
                                                                 requestQuery)

        block, filterResponse = await FilterManager.HeaderFilter.execute(respHeader, config, False)
        if block is True:
            return filterResponse

        block, bodyFilterResponse = await FilterManager.BodyFilter.execute(respBody, config, False)
        if block is True:
            return bodyFilterResponse

        replacedHeader = await ReplaceManager.HeaderReplacer.execute(respHeader, config, False)
        replacedBody = await ReplaceManager.BodyReplacer.execute(respBody, config, False)

        response = web.StreamResponse(headers=replacedHeader, status=respStatus)
        response.content_type = "text/tab-separated-values; charset=utf-8"
        await response.prepare(request)
        await response.write(replacedBody.encode("utf-8"))
        print(f"Response HeadeR:{response.headers}")

        return response


    app = web.Application()
    app.add_routes(routes)

    if config.get('ssl').get('enable') is True:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(config.get('ssl').get('cert'), config.get('ssl').get('key'))
        web.run_app(app, host=config.get('url').get('ip_address').split(':')[0],
                    port=config.get('url').get('ip_address').split(':')[1], ssl_context=ssl_context)
    else:
        web.run_app(app, host=config.get('url').get('ip_address').split(':')[0],
                    port=config.get('url').get('ip_address').split(':')[1])
