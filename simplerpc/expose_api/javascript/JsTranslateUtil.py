# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.expose_api.javascript.base import JsTranslatorBase

class JsTranslateUtil(JsTranslatorBase):
  '''
  #TODO: document
  '''

def smokeTestModule():
  from example_rpc.exposed_api.images.ImagesBrowser import ImagesBrowser
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  from simplerpc.SimpleRpcError import SimpleRpcError
  context = SimpleRpcContext('smoke test')
  context.log(JsTranslateUtil(context)._getJsNamespace(ImagesBrowser))
  for o in [context, JsTranslatorBase]:
    try:
      JsTranslateUtil(context)._getJsNamespace(o)
    except SimpleRpcError:
      pass

if __name__ == "__main__":
  smokeTestModule()
