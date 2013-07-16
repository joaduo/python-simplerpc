# -*- coding: utf-8 -*-
'''
Copyright (c) 2013, LastSeal S.A.
Copyright (c) 2011-2012, Joaquin G. Duo
All rights reserved.

This code is distributed under BSD 3-clause License. 
For details check the LICENSE file in the root of the project.
'''
from simplerpc.common.abstract.ContextClientBase import ContextClientBase
from simplerpc.common.context.ConfigWrapper import ConfigWrapper

#TODO: rename to ClassConfigBase
class SelfConfigBase(ContextClientBase):
  '''
    They will do to save some config:
      self.config.some_parameter = <value>
    And to retrieve it:
      <variable> = self.config.some_parameter
    Where 'self' would be an instance of the owner class (OwnerClass).
    Without this wrapper the class should have to do:
      <variable> = self.context.get_config(self.__class__,'some_parameter')
    This way, accessing to the config is straightforward. 

  '''  
  def __init__(self, context):
    ContextClientBase.__init__(self, context)
    #TODO: rename it to class_config?
    self.config = ConfigWrapper(owner_class=self.__class__, context=self.context)
    self.log = self.context.log

def smokeTestModule():
  ''' Simple self-contained test for the module '''    
  from simplerpc.common.context.base import ContextBase
  class Context(ContextBase):
    def _loadInitConfig(self):
      pass

  class FooTestPluginsManager(SelfConfigBase):
    def __post_init__(self):
      self.processors = {}  

  ctx = Context('smoke test')
  pm= FooTestPluginsManager(context=ctx)
  assert pm.config
  pm.config.hola = 'valor'
  assert pm.config.hola == 'valor'
  try:
    pm.config.context = 'bla'
  except AttributeError as e:
    pass

if __name__ == '__main__':
  smokeTestModule()
