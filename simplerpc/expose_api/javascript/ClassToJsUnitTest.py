# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.expose_api.javascript.ClassToJs import ClassToJs
from simplerpc.expose_api.javascript.TemplatesCollector import TemplatesCollector
from string import Template
import os
from simplerpc.common.FileManager import FileManager

class ClassToJsUnitTest(SimpleRpcLogicBase):
  '''
  #TODO: document
  '''
  def __post_init__(self):
    self.class_to_js = ClassToJs(self.context)
    self.templates = TemplatesCollector(self.context)
    self.file_manager = FileManager(self.context)

  def translateClass(self, class_):
    '''  '''
    ast_tree = self.class_to_js.translateClass(class_)
    templates_set = 'js_unittest_templates'
    templates = self.templates.collectBuiltIn(templates_set)
    js_str = ast_tree.getString(templates)
    return js_str

  def translateToFile(self, tested_class, file_path, overwrite=False):
    js_str = self.__getClassJsUnit(tested_class)
    #create directory just in case
    test_dir = os.path.dirname(file_path)
    self.file_manager.makedirs(test_dir)
    #Say where it is in a pretty way
    path = self.file_manager.formatFilePath(file_path)
    name = tested_class.__name__
    self.log.d('Creating js for %s test at:\n %s' % (name, path))
    #save file
    self.file_manager.saveTextFile(file_path, js_str, overwrite)

  def __getClassJsUnit(self, tested_class):
    js_str = self.translateClass(tested_class)
    translate = dict(EXPOSED_RPC_API_CLASS=self.context.js_rpc_file)
    js_str = Template(js_str).safe_substitute(translate)
    return js_str


def smokeTestModule():
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('smoke test')
  from example_rpc.exposed_api.images.ImagesBrowser import ImagesBrowser
  js_str = ClassToJsUnitTest(context).translateClass(ImagesBrowser)
  context.log(js_str)

if __name__ == "__main__":
  smokeTestModule()
