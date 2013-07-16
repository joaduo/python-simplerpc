# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from inspect import isclass
from simplerpc.SimpleRpcError import SimpleRpcError
from types import ModuleType
import os
from simplerpc.common.path import joinPath
from importlib import import_module

class JsTranslatorBase(SimpleRpcLogicBase):
  '''
  Base class for Python to Javascript translation
  '''
  def _getProjectJsPath(self):
    if os.path.isabs(self.context.js_path):
      js_root = self.context.js_path
    else:
      js_root = joinPath(self._getProjectPath(), self.context.js_path)
    return js_root

  def _getJsRpcFile(self, js_rpc_file):
    if not js_rpc_file:
      js_rpc_file = joinPath(self._getProjectJsPath(), self.context.js_rpc_file)
    elif not os.path.isabs(js_rpc_file):
      js_rpc_file = joinPath(self._getProjectJsPath(), js_rpc_file)
    return js_rpc_file

  def __getModuleNamespace(self, module_name):
    #For example
    #example_rpc.exposed_api.images.ImagesBrowser
    #we need to get rid of example_rpc.exposed_api
    module = import_module(module_name)
    path = os.path.splitext(module.__file__)[0]
    prefix = None
    for pkg in self.context.exposed_roots:
      prefix = os.path.dirname(pkg.__file__)
      if os.path.commonprefix((prefix, path)) == prefix:
        break
      else:
        prefix = None
    if not prefix:
      msg = 'Cannot create namespace. Module %r not in %r' % \
            (module, self.context.exposed_roots)
      raise SimpleRpcError(msg)
    namespace = os.path.relpath(path, prefix)
    return namespace

  def _getJsNamespace(self, py_obj):
    '''
    Gets the Javascript namespace corresponding to an exposed class o module.

    :param py_obj: class or module to be exposed
    '''
    if isclass(py_obj):
      #If its a class then use its module name
      return self.__getModuleNamespace(py_obj.__module__)
    elif isinstance(py_obj, ModuleType):
      #Its a module, then directly use its name
      return self.__getModuleNamespace(py_obj.__name__)
    else:
      raise SimpleRpcError('No way to create RPC namespace for object %r' % py_obj)

def smokeTestModule():
  from example_rpc.exposed_api.images.ImagesBrowser import ImagesBrowser
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('smoke test')
  context.log(JsTranslatorBase(context)._getJsNamespace(ImagesBrowser))
  for o in [context, JsTranslatorBase]:
    try:
      JsTranslatorBase(context)._getJsNamespace(o)
    except SimpleRpcError:
      pass

if __name__ == "__main__":
  smokeTestModule()
