# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
import logging
from simplerpc.common.context.base import ContextBase, context_singleton

@context_singleton
class SimpleRpcContext(ContextBase):
  def __init__(self, name, settings=None):
    if not settings:
      settings = self.__getProjectSettings()
    self.__settings = settings
    ContextBase.__init__(self, name)

  def _loadInitConfig(self):
    config = self.__settings.getConfigDict()
    for name, value in config.items():
      self.set_config(name, value)

  def __getProjectSettings(self):
    try:
      from simplerpc_settings import Settings
      return Settings()
    except ImportError as error:
      logging.error(error)
      raise error

def smokeTestModule():
  context = SimpleRpcContext('webserver')
  context.log(context)

if __name__ == "__main__":
  smokeTestModule()
