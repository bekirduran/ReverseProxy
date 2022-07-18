import argparse

import toml
from aiohttp import web

from App.Server.DeleteHandler import DeleteHandler
from App.Server.GetHandler import GetHandler
from App.Server.PostHandler import PostHandler
from App.Server.PutHandler import PutHandler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="aiohttp server example")
    parser.add_argument('--toml', type=str, help='toml file path', default='../server.toml')
    parser.add_argument('-i', '--ip_address', type=str, help='server ip', default='192.168.30.5')
    args = parser.parse_args()
    config = toml.load(args.toml)

    app = web.Application()
    routes = web.RouteTableDef()

    GetHandler.execute(routes,config)
    PostHandler.execute(routes,config)
    PutHandler.execute(routes,config)
    DeleteHandler.execute(routes,config)

    app.add_routes(routes)
    web.run_app(app, host=args.ip_address,port=3000)
