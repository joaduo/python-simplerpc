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
  Inherit from this class if you want to automatically expose decorated method.
  Available decorators are in simple_rpc.expose_api.decorators.

  Classes are exposed in the same namespace they have in python.
  For example:
    example_rpc.exposed_api.images.ImagesBrowser.getImagesList
  will end in:
    exposed_api.images.ImagesBrowser.getImagesList

  Where 'exposed_api' comes from:
    var context = require('context').getContext();
    var exposed_api = require('example_rpc/ExposedRpcApi')(context).getApiRoot();
    //you use it
    exposed_api.images.ImagesBrowser.getImagesList(...);

  You can also access to exposed API in javascript in a more nodejs way:
    ImagesBrowser = require('example_rpc/ExposedRpcApi')(context
                    ).requireApi('images/ImagesBrowser');

  '''
  def __init__(self):
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
