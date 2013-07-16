# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.common.python3 import portable_getargspec
from simplerpc.expose_api.javascript.base import JsTranslatorBase
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.expose_api.javascript.data_model import TranslationAstNode, \
  AutoTemplateAstNode
from simplerpc.expose_api.decorators import getDecoratorsDict
from simplerpc.context.SimpleRpcContext import SimpleRpcContext

class ClassToJs(JsTranslatorBase):
  '''
  Translate a Python class Into a Exposed Class in Javascript
  Creates a Translation AST of the class.
  '''
  def translateClass(self, class_):
    class_namespace = self._getJsNamespace(class_)
    class_node = TranslationAstNode('classes.ExposedClass')
    class_node.translate(CLASS_NAME=class_.__name__,
                         NAMESPACE='/'.join(class_namespace.split('.')))
    #TODO: clean this
    decorators = [name for name in getDecoratorsDict().keys()
                  if not name.startswith('private')]
    methods_node = AutoTemplateAstNode()
    for method_type in decorators:
      m = self._getMethodTypeNode(class_, class_namespace, method_type)
      if m:
        methods_node.translate(method_type, m)
    class_node.translate(METHODS=methods_node)
    return class_node

  def _getArgsJs(self, method_args):
    args_string = ' ,'.join(method_args)
    if args_string != '':
      args_string += ','
    return args_string

  def _getKwargsJs(self, method_args):
    kwargs_string = ''
    for arg in method_args:
      kwargs_string += '%r:%s,' % (arg, arg)
    return kwargs_string

  def _getClassInstance(self, class_):
    if issubclass(class_, SimpleRpcLogicBase):
      return class_(self.context)
    else:
      return class_()

  def _getMethodTypeNode(self, class_, class_namespace, method_type):
    methods_node = AutoTemplateAstNode()
    instance = self._getClassInstance(class_)
    exposed_methods = instance.exposedMethods(method_type)
    if len(exposed_methods):
      for method_name in exposed_methods:
        mt_node = TranslationAstNode('methods.%s' % method_type)
        method = getattr(instance, method_name)
        if hasattr(method, 'method'): #TODO should look for getDecoratedMethod
          method = method.method

        method_args = portable_getargspec(method)[0][1:]
        cmd_string = class_namespace + '.' + method_name

        mt_node.translate(METHOD_NAME=method_name,
                          ARGS=self._getArgsJs(method_args),
                          KWARGS=self._getKwargsJs(method_args),
                          RPC_METHOD=cmd_string,)
        methods_node.translate(method_name, mt_node)
      return methods_node
    else:
      return None

def smokeTestModule():
  context = SimpleRpcContext('smoketest')

  ctjt = ClassToJs(context)

  from example_rpc.exposed_api.images.ImagesBrowser import ImagesBrowser
  tree = ctjt.translateClass(ImagesBrowser)
  context.log(tree)
  from simplerpc.expose_api.javascript.TemplatesCollector import TemplatesCollector
  templates = TemplatesCollector(context).collectBuiltIn()
  context.log(tree.getString(templates))


if __name__ == "__main__":
  smokeTestModule()

