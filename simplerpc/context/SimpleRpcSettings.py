# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcObject import SimpleRpcObject

class SimpleRpcSettings(SimpleRpcObject):
  def getConfigDict(self):
    config_dict = dict()
    for name in dir(self):
      if not name.startswith('_'):
        value = getattr(self, name)
        if not callable(value):
          config_dict[name] = value
    return config_dict

def smokeTestModule():
  SimpleRpcSettings()
  import example_rpc
  from simplerpc.common.path import joinPath

  class Settings(SimpleRpcSettings):
    #determines the project path and all relative modules in this package
    project_package = example_rpc
    #if relative, its relative to the project package path
    js_path = './webclient/static/js'
    #Where the exposed rpc api class is stored
    js_rpc_file = joinPath(example_rpc.__name__, 'ExposedRpcApi.js')

  from simplerpc.common.log.printSmoke import printSmoke
  printSmoke(Settings().getConfigDict())

if __name__ == "__main__":
  smokeTestModule()
