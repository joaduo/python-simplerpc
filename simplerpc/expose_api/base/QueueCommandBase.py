# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.expose_api.base.ExposedBase import ExposedBase
from simplerpc.expose_api.decorators import expose, decorator_base

class QueueCommandBase(ExposedBase):
  '''
  Inherit from this class to expose each non-decorated method via POST
  interface. (they are not marked idempotent neither safe)
  For safe and idempotent methods mark them manually. See documentation in
  `class:simplerpc.expose_api.base.ExposedBase.ExposedBase`
  '''
  def _getMethodFilterFunc(self, decorator_class):
    #crate filter to accept automatically non decorated public methods as exposed
    basic_filter = ExposedBase._getMethodFilterFunc(self, decorator_class)
    def filterFunc(name, decorator):
      return not name.startswith('_') and decorator_class == expose \
             and not isinstance(decorator, decorator_base) or \
             basic_filter(name, decorator)
    return filterFunc

def smokeTestModule():
  from simplerpc.common.log.printSmoke import printSmoke
  class TestExpose(QueueCommandBase):
    def test(self):
      return 1
    @expose.safe
    def test2(self):
      pass
  te = TestExpose()
  printSmoke(te.exposedMethods(expose))
  printSmoke(te.exposedMethods(expose.safe))

if __name__ == "__main__":
  smokeTestModule()
