# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from types import MethodType

class rpc_decorator_base(object):
  def __init__(self, method):
    self.method = method
  def __call__(self, *args, **kwargs):
    return self.method(*args, **kwargs)
  def __get__(self, obj, objtype=None):
    return MethodType(self, obj, objtype)  

class public_readonly(rpc_decorator_base):
  pass

class public_get(rpc_decorator_base):
  pass

class public_post(rpc_decorator_base):
  pass

class private_readonly(rpc_decorator_base):
  pass

class private_get(rpc_decorator_base):
  pass

class private_post(rpc_decorator_base):
  pass

#TODO: automate below?
def getDecoratorsList():
  return [ public_readonly, 
           public_get, 
           public_post,
           private_readonly,
           private_get,
           private_post ]

def getDecoratorsDict():
  decorators = getDecoratorsList()
  decorators_dict = {}
  for dec in decorators:
    decorators_dict[dec.__name__] = dec
  return decorators_dict


def smokeTestModule():
  getDecoratorsDict()
  getDecoratorsList()

if __name__ == "__main__":
  smokeTestModule()

