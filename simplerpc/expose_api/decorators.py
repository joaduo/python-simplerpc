# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from types import MethodType

class decorator_base(object):
  pass

def getClass(name):
  class ExposedDecorator(decorator_base):
    def __init__(self, method):
      self.method = method
    def __call__(self, *args, **kwargs):
      return self.method(*args, **kwargs)
    def __get__(self, obj, objtype=None):
      return MethodType(self, obj, objtype)
  return ExposedDecorator

class expose(getClass('expose')):
  safe = getClass('safe')
  idempotent = getClass('idempotent')

def getDecoratorsList():
  return [expose, expose.safe, expose.idempotent]

def smokeTestModule():
  @expose
  def function():
    pass
  @expose.safe
  def function2():
    pass
  @expose.idempotent
  def function3():
    pass

if __name__ == "__main__":
  smokeTestModule()

