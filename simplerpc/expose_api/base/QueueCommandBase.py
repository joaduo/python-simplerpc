# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.expose_api.base.ExposedBase import ExposedBase

class QueueCommandBase(ExposedBase):
  def exposedMethods(self, method_type='public_post'):
    def filter_func(name):
      method = getattr(self, name)
      return callable(method) and not name.startswith('_')
    if method_type == 'public_post':
      return self._exposedMethods(method_type, filter_func)
    else:
      return self._exposedMethods(method_type, filter_func=None)

def smokeTestModule():
  from simplerpc.common.log.printSmoke import printSmoke
  class TestExpose(QueueCommandBase):
    def test(self):
      return 1
  te = TestExpose()
  printSmoke(te.exposedMethods('public_post'))
  
if __name__ == "__main__":
  smokeTestModule()
