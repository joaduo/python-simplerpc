# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.common.abstract.decorators.context_singleton import context_singleton
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.RpcNotFoundError import RpcNotFoundError
from simplerpc.context.SimpleRpcContext import SimpleRpcContext
from simplerpc.expose_api.ExposedPackageBrowser import ExposedPackageBrowser
from simplerpc.expose_api.javascript.JsTranslateUtil import JsTranslateUtil
from importlib import import_module
from inspect import isclass
from simplerpc.SimpleRpcError import SimpleRpcError
from simplerpc.expose_api.decorators import getDecoratorsList

@context_singleton
class RPCDispatcher(SimpleRpcLogicBase):
  '''
  Creates the dispatching dictionary.
  Then answers incoming commands already converted to python.
  Each requested command must exist in the dispatch dictionary.
  '''
  def __post_init__(self, packages, constructor_kwargs={}):
    #we need the package browser to build the dispatch dicitonary
    self.package_browser = ExposedPackageBrowser(self.context)
    #we need to know how a module is called in javascript (thus a command)
    self.js_util = JsTranslateUtil(self.context)
    #we can now build the dispatch dictionary
    self.__dispatch_dict = self.__buildDispatchDict(packages, constructor_kwargs)

  def __buildDispatchDict(self, packages, constructor_kwargs):
    exposed = self.context.exposed_roots
    handlers_dict = {}
    for root_package, sub_packages in packages.items():
      if root_package not in exposed:
        msg = 'Root package %s is not exposed in the simplerpc_settings' % \
              root_package.__name__
        raise SimpleRpcError(msg)
      self.__buildPackageDict(root_package, sub_packages,
                              constructor_kwargs, handlers_dict)
    return handlers_dict

  def __buildPackageDict(self, root_package, sub_packages, constructor_kwargs,
                         handlers_dict):
    modname_prefix = root_package.__name__
    for package_name in sub_packages:
      self.log.d('Importing module %s.%s as RPC handler.' % (modname_prefix,
                                                             package_name))
      package = import_module('%s.%s' % (modname_prefix, package_name))
      self.__getPackageHandlers(package, self.__getDecorators(), handlers_dict,
                                constructor_kwargs)
    return handlers_dict

  def __getDecorators(self):
    decorators = getDecoratorsList()
    dec_dict = dict()
    for dec in decorators:
      dec_dict[dec.__name__] = dec
    return dec_dict

  def __getPackageHandlers(self, package, decorators, handlers_dict,
                           constructor_kwargs):
    classes = self.package_browser.getModuleAndClass(package)
    for module, class_ in classes:
      instance = class_(**constructor_kwargs)
      class_namespace = self.js_util._getJsNamespace(module)
      for dec_name, dec in decorators.items():
        if dec_name not in handlers_dict:
          handlers_dict[dec_name] = {}
        for method_name in instance.exposedMethods(dec):
          cmd_str = '.'.join([class_namespace, method_name])
          handlers_dict[dec_name][cmd_str] = getattr(instance, method_name)
    return handlers_dict

  def answer(self, decorator_class, cmd, args, kwargs):
    if isclass(decorator_class): #we got a decorator class, convert to string
      decorator_class = decorator_class.__name__

    if decorator_class in self.__dispatch_dict \
      and cmd in self.__dispatch_dict[decorator_class]:
      method = self.__dispatch_dict[decorator_class][cmd]
    else:
      raise RpcNotFoundError('Command %r of type %r not exposed or existent.'
                             % (cmd, decorator_class))

    return_value = method(*args, **kwargs) #TODO: security review?
    return return_value

def smokeTestModule():
  context = SimpleRpcContext('test')
  import example_rpc.exposed_api as exposed_api
  rd = RPCDispatcher(context, packages={exposed_api:['images']})

if __name__ == "__main__":
  smokeTestModule()


