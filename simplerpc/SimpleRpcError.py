# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''

class SimpleRpcError(Exception):
    pass

def smokeTestModule():
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    context = SimpleRpcContext('smoke test')
    msg = 'Some msg'
    try:
        raise SimpleRpcError(msg)
    except SimpleRpcError as e:
        assert str(e) == msg
        context.log.d(e)

if __name__ == "__main__":
    smokeTestModule()
