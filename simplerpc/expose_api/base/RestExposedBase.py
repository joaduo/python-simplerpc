# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.expose_api.base.ExposedBase import ExposedBase

class RestExposedBase(ExposedBase):
  def exposedMethods(self, method_type=None):
    method_names = set(['create', 'read', 'update', 'delete',])
    attributes = self.__class__.__dict__
    exposed_methods = []
    for name, attrib in attributes.items():
      if name in method_names:
        assert callable(attrib), 'REST method {name} of class {self.__class__} is not callable.'.format(locals())
        exposed_methods.append(attrib)
    return exposed_methods

def smokeTestModule():
  pass
  
if __name__ == "__main__":
  smokeTestModule()
