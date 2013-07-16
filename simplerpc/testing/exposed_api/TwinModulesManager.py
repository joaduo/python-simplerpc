# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.common.path import realPath, splitPath, joinPath
import os
from unittest.case import TestCase

class TwinModulesManager(SimpleRpcLogicBase):
  '''
  Solves Twin modules names so that it's easy to find the twin module from one
  module.
  Each project class will/can have a twin test module. (same name, same
  hierachy in but with some other prefix)
  In the case of exposed classes the can also have a javascript unit test twin.
  This class solves:
    - tested_class <-> tester_class (both ways)
    - tested_class or tester_class  -> javascript unit test file
  '''
  #relative prefix from the project package
  tests_relative_prefix = 'tests.twin_unittests.'
  def getTestedFromTester(self, tester_class):
    #Get tested module name
    tested_module_name = self.__getClassModuleName(tester_class)
    #remove the unit test package prefix
    tested_module_name = tested_module_name[len(self.tests_relative_prefix):]
    #import the class from module
    return self.__importClass(tested_module_name)

  def getTesterFromTested(self, tested_class):
    #Add add unit test package prefix to tested class
    tester_module_name = self.tests_relative_prefix + \
                         self.__getClassModuleName(tested_class)
    #import the class from module
    return self.__importClass(tester_module_name)

  def __getClassModuleName(self, class_):
    if class_.__module__ == '__main__':
      import __main__ as module
      project_package_path = realPath(self.context.project_package.__path__[0])
      module_file_path = os.path.splitext(realPath(module.__file__))[0]
      if module_file_path.startswith(project_package_path):
        module_name = '.'.join(splitPath(module_file_path)
                               [len(splitPath(project_package_path)):])
    else:
      module_name = class_.__module__[len(self.__baseName()) + 1:]
    return module_name

  def __baseName(self):
    return self.context.project_package.__name__

  def __addProjectPrefix(self, module_name):
    return '%s.%s' % (self.__baseName(), module_name)

  def __importClass(self, module_name):
    module_name = self.__addProjectPrefix(module_name)
    class_name = module_name.split('.')[-1]
    module = __import__(module_name, fromlist='dummy')
    class_ = getattr(module, class_name)
    return class_

  def getJsUnittest(self, class_):
    #solve to the tested class if not given
    if issubclass(class_, TestCase):
      tested_class = self.getTestedFromTester(class_)
    else:
      tested_class = class_
    module_name = self.__getClassModuleName(tested_class)
    if os.path.isabs(self.context.js_path):
      js_prefix = self.context.js_path
    else:
      js_prefix = joinPath(self._getProjectPath(), self.context.js_path)
    #create path and add unittests folder inside the js folder
    test_path = joinPath(js_prefix, 'unittests', module_name.split('.'))
    #add extension
    test_path += '.js'
    return test_path


def smokeTestModule():
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('smoke test')
  from example_rpc.exposed_api.images.ImagesBrowser import ImagesBrowser
  twinm = TwinModulesManager(context)
  context.log(twinm.getJsUnittest(ImagesBrowser))
#  tested_class = TwinModulesManager(context).getJsUnittest(tester_class)

if __name__ == "__main__":
  smokeTestModule()
