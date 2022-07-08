import argparse
import ssl
import toml
from aiohttp import web

from App.Server.DeleteHandler import DeleteHandler
from App.Server.GetHandler import GetHandler
from App.Server.PostHandler import PostHandler
from App.Server.PutHandler import PutHandler

parser = argparse.ArgumentParser(description="aiohttp server example")
args = parser.parse_args()
parser.add_argument('--ip')
config = toml.load('../config.toml')

app = web.Application()
routes = web.RouteTableDef()

GetHandler.execute(routes)
PostHandler.execute(routes)
PutHandler.execute(routes)
DeleteHandler.execute(routes)


app.add_routes(routes)
args.ip = '192.168.30.7'
if config.get('ssl').get('enable') is True:
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(config.get('ssl').get('cert'), config.get('ssl').get('key'))
    web.run_app(app, host=args.ip, ssl_context=ssl_context)
else:
    web.run_app(app, host=args.ip)
