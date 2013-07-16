# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.SimpleRpcError import SimpleRpcError

class RpcNotFoundError(SimpleRpcError):
  '''
  #TODO: document, implement
  '''

def smokeTestModule():
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('smoke test')

  msg = 'Some msg'
  try:
    raise RpcNotFoundError(msg)
  except RpcNotFoundError as e:
    assert str(e) == msg
    context.log.d(repr(e))

if __name__ == "__main__":
  smokeTestModule()
