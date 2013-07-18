#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
Copyright (c) 2012-2013, LastSeal S.A.
'''

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path
from tornado.options import define, options
from example_rpc.tornado_handler.RPCRequestHandler import RPCRequestHandler
from simplerpc.context.SimpleRpcContext import SimpleRpcContext
from simplerpc.expose_api.javascript.RPCJavascriptGenerator import RPCJavascriptGenerator
from example_rpc.tornado_handler.JsonRpcHandler import JsonRpcHandler

#import logging
#logging.disable(logging.INFO)
#logging.disable(logging.WARNING)

define("port", default=8002, help="run on the given port", type=int)

class Application(tornado.web.Application):
  def __init__(self):
    handlers = [
      (r"/", MainHandler),
      (r"/public_readonly/.*", JsonRpcHandler),
      (r"/commands_queue/.*", JsonRpcHandler),
    ]
    settings = dict(
      template_path=os.path.join(self.getWebClientRoot(), "templates"),
      static_path=os.path.join(self.getWebClientRoot(), "static"),
      debug=True, #TODO: configurable
    )
    tornado.web.Application.__init__(self, handlers, **settings)
    self.__generateJsRpc()

  def __generateJsRpc(self):
    context = SimpleRpcContext('js_translator')
    context.log('Translating Js RPC...')
    #packages
    import example_rpc.exposed_api.images
    packages = [example_rpc.exposed_api.images]
    RPCJavascriptGenerator(context).translateToFile(packages, overwrite=True)
    context.log('Done.')

  def getWebClientRoot(self):
    return './example_rpc/webclient'

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    self.render("index.html")

if __name__ == "__main__":
  tornado.options.parse_command_line()
  http_server = tornado.httpserver.HTTPServer(Application())
  http_server.listen(options.port)
  tornado.ioloop.IOLoop.instance().start()

