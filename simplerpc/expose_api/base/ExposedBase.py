# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.base.SimpleRpcObject import SimpleRpcObject

class ExposedBase(SimpleRpcObject):
  '''
  Inherit from this class if you want to automatically expose decorated method.
  Available decorators are in simple_rpc.expose_api.decorators.
  To be exposed methods must:
    - be public -> not starting with "_" (underscore)
    - belonging to the Leaf class (methods of parent classes wont be published)
  If you would like to override this policies inherit from this class and
  re-implement the "_getMethodFilterFunc" or "exposedMethods"  method.

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
  def exposedMethods(self, decorator_class):
    '''
    Returns a list of names of the decorated methods for this class
    :param decorator_class: decorator_class class inspected
    '''
    filter_func = self._getMethodFilterFunc(decorator_class)
    return self._exposedMethods(filter_func)

  def _getMethodFilterFunc(self, decorator_class):
    return lambda name, decorator: isinstance(decorator, decorator_class)

  def _exposedMethods(self, filter_func):
    ''' Will only expose methods of the leaf classes to avoid security risks.
        By default not decorated methods will be taken as
    '''
    names = self.__class__.__dict__.keys()
    exposed_methods = []
    for name in names:
      method = getattr(self, name)
      if filter_func(name, method):
        exposed_methods.append(name)
    return exposed_methods

def smokeTestModule():
  from simplerpc.common.log.printSmoke import printSmoke
  from simplerpc.expose_api.decorators import expose
  class TestExpose(ExposedBase):
    @expose
    def test(self):
      return 1
    @expose.safe
    def get(self):
      pass
    @expose.idempotent
    def delete(self):
      pass
  te = TestExpose()
  printSmoke(te.exposedMethods(expose))
  printSmoke(te.exposedMethods(expose.idempotent))
  printSmoke(te.exposedMethods(expose.safe))

if __name__ == "__main__":
  smokeTestModule()
