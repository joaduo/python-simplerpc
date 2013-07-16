# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.SimpleRpcError import SimpleRpcError
from simplerpc.expose_api.decorators import getDecoratorsDict, rpc_decorator_base
from simplerpc.base.SimpleRpcObject import SimpleRpcObject

class ExposedBase(SimpleRpcObject):
  '''
  #TODO: document
  Introspect to expose the public methods through RPC API
  Introspect to generate the API in javascript to call the RPC API
  '''
  def __init__(self):
    ''' #TODO: document '''
    self.decorators = getDecoratorsDict()

  def exposedMethods(self, method_type):
    return self._exposedMethods(method_type, filter_func=None)

  def _exposedMethods(self, method_type, filter_func):
    ''' Will only expose methods of the child class to avoid security risks.
        By default not decorated methods will be taken as
    '''
    if not method_type in self.decorators:
      raise SimpleRpcError('There is no method type %r. Availables: %s' % (method_type, self.decorators.keys()))
    decorator_class = self.decorators[method_type]
    attributes = self.__class__.__dict__
    exposed_methods = []
    for name, value in attributes.items():
      if isinstance(value, decorator_class):
        exposed_methods.append(name)
      elif not isinstance(value, rpc_decorator_base) and filter_func and filter_func(name):
        exposed_methods.append(name)
    return exposed_methods

def smokeTestModule():
  from simplerpc.common.log.printSmoke import printSmoke
  from simplerpc.expose_api.decorators import public_post
  class TestExpose(ExposedBase):
    @public_post
    def test(self):
      return 1
  te = TestExpose()
  printSmoke(te.exposedMethods('public_post'))

if __name__ == "__main__":
  smokeTestModule()
