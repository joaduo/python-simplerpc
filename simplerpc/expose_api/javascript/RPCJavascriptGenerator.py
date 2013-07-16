# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.expose_api.javascript.PackageToJs import PackageToJs
from simplerpc.common.FileManager import FileManager
from simplerpc.expose_api.javascript.data_model import TranslationAstNode, \
  AutoTemplateAstNode
from simplerpc.expose_api.javascript.TemplatesCollector import TemplatesCollector
from simplerpc.expose_api.javascript.JsTranslateUtil import JsTranslateUtil

class RPCJavascriptGenerator(SimpleRpcLogicBase):
  def __post_init__(self):
    self.file_manager = FileManager(self.context)
    self.package_translator = PackageToJs(self.context)
    self.templates_collector = TemplatesCollector(self.context)
    self.js_util = JsTranslateUtil(self.context)

  def getRpcNode(self, packages):
    packages_node = AutoTemplateAstNode()
    for p in packages:
      n = self.package_translator.translatePackage(p)
      name = p.__name__.split('.')[-1]
      packages_node.translate(name, n)
    exposed_rpc_node = TranslationAstNode('exposed_rpc.CommandQueueApi')
    exposed_rpc_node.translate(EXPOSED_PACKAGES=packages_node)
    return exposed_rpc_node

  def translateToFile(self, packages, js_rpc_file=None, templates=None,
                      overwrite=False):
    js_rpc_file = self.js_util._getJsRpcFile(js_rpc_file)
    if not templates:
      templates = self.templates_collector.collectBuiltIn()
    text = self.getRpcNode(packages).getString(templates)
    self.file_manager.saveTextFile(js_rpc_file, text, overwrite)

def smokeTestModule():
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('smoke test')
  import example_rpc.exposed_api.images
  packages = [example_rpc.exposed_api.images]
  tree = RPCJavascriptGenerator(context).getRpcNode(packages)
  templates = TemplatesCollector(context).collectBuiltIn()
  context.log.d(tree.getString(templates))

if __name__ == "__main__":
  smokeTestModule()



