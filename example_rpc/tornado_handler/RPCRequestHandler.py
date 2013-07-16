# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.expose_api.RPCDispatcher import RPCDispatcher
from simplerpc.expose_api.decorators import public_readonly, public_get, public_post
from simplerpc.SimpleRpcError import SimpleRpcError
import tornado.web
import json
from simplerpc.context.SimpleRpcContext import SimpleRpcContext

class RPCRequestHandler(tornado.web.RequestHandler):
  '''
  This is the main handler for Dispatching commands from the auto-generated
  Javascript API.
  self.dispatcher is responsible of creating a dispatching dict and doing the
  distpatch.
  '''
  def __init__(self, *args, **kwargs):
    tornado.web.RequestHandler.__init__(self, *args, **kwargs)
    #Create a context
    self.context = SimpleRpcContext('examplerpc_tornado')
    #Init dispatcher dictionary
    import example_rpc.exposed_api as exposed_api
    self.dispatcher = RPCDispatcher(self.context, packages={exposed_api:['images']})

  def _delistArguments(self, arguments):
    '''
    Requests arguments comes in a list if they are declared twice (POST and
    GET for example). Choose only one.
    :param arguments:
    '''
    def filterFunc(name, value):
      if len(value) > 1:
        self.context.log.d('Receiving more than one value for argument %r '
                           '(values:%r). Using first value.' % (name, value))
      return True
    items = [(name, val[0]) for name, val in  self.request.arguments.items()
             if filterFunc(name, val)]
    return dict(items)

  def get(self):
    '''
    Serve all GET requests and dispatch them to their corresponding class.
    '''
    uri_split = self.request.uri.split('?')[0].split('/')
    method_type = uri_split[1]
    cmd = '.'.join(uri_split[2:])
    if method_type == 'public_readonly':
      kwargs = self._delistArguments(self.request.arguments)
      return_value = self.dispatcher.answer(public_readonly, cmd=cmd, args=[],
                                            kwargs=kwargs)
    elif method_type == 'public_get':
      kwargs = self._delistArguments(self.request.arguments)
      return_value = self.dispatcher.answer(public_get, cmd=cmd, args=[],
                                            kwargs=kwargs)
    #TODO: 'private_get':
    else:
      raise SimpleRpcError('Unknown method_type %r...' % method_type[:10])

    self.write(dict(return_value = return_value))
    self.finish()

  def post(self):
    '''
    Serve all POST requests and dispatch them to their corresponding class.
    '''
    uri_split = self.request.uri.split('?')[0].split('/')
    method_type = uri_split[1]
    if method_type == 'commands_queue':
      cmds = json.loads(self.get_argument('cmds'))
      results = self._execCommandsQueue(cmds)
      self.write(dict(results = results))
    #TODO: elif method_type == 'public_post': #TODO: 'private_post':
    else:
      raise SimpleRpcError('Unknown method_type %r...' % method_type[:10])

    self.finish()

  def _execCommandsQueue(self, cmds):
    '''
    If a command queue comes, we need to answer each command trapping
    exceptions and reporting errors for each command.
    :param cmds:list of commands sent by the client.
    '''
    results = []
    for cmd in cmds:
      name_index, args_index, kwargs_index = 0, 1, 2
      try:
        return_value = self.dispatcher.answer(public_post, cmd[name_index], cmd[args_index], cmd[kwargs_index])
        error = None
      except Exception as e:
        return_value = None
        error = str(e)
      results.append(dict(return_value = return_value, error = error))
    return results

def smokeTestModule():
  pass

if __name__ == "__main__":
  smokeTestModule()
