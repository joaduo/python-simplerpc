# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
#from simplerpc.common.path import joinPath, splitPath
#from simplerpc.expose_api.decorators import getDecoratorsDict
from unittest.runner import TextTestRunner
from unittest.loader import TestLoader
#import os

class ModuleUnitTestRunner(SimpleRpcLogicBase):

  def runTestByNumber(self, package, test_number):
    tests_dict = self._getTestDict()
    sorted_names = self.__getSortedNames(tests_dict)
    new_dict = dict((module.__name__, class_) for module, class_ in tests_dict.items())
    tester_class = new_dict[sorted_names[test_number]]
    self.runSingleTest(tester_class)

  def __runUnitTest(self, tester_class):
    tester_class.setTestsContext(self.context)
    suite = TestLoader().loadTestsFromTestCase(tester_class)
    TextTestRunner().run(suite)

  def runSingleTest(self, tester_class, tested_class, run_javascript=True):
    self.__runUnitTest(tester_class)
    #self.log.d('Testing class %r'%tester_class)
    #tester_instance = tester_class(self.context)

    #.run(tester_instance)
    #tested_instance = tested_class(self.context)
#    if hasattr(tester_instance, 'setUp'):
#      tester_instance.setUp()
#    tester_instance.run()
#    if run_javascript:
#      self.__runJavascriptTwin(tester_instance, tested_instance, self.__getJavascriptTwin(tester_class))
#    if hasattr(tester_instance, 'tearDown'):
#      tester_instance.tearDown()

#  def __getJavascriptTwin(self, tester_class):
#    module_path = tester_class.__module__
#    javascript_test_path = ''
#    modules_tests_path = self.context.config.modules_tests_path
#    if module_path.startswith(modules_tests_path):
#      javascript_test_path = module_path[len(modules_tests_path) + 1:]
#      javascript_test_path = joinPath(self.context.config.rpc_api_tests_path, javascript_test_path.split('.'))
#    return javascript_test_path
#
#  def __runJavascriptTwin(self, tester_instance, tested_instance, javascript_test_path):
#    command_runner = CommandRunner(self.context)
#    base_path = self.context.project_path
#    run_rpc_api_tests_path = joinPath(base_path, self.context.config.run_rpc_api_tests_path)
#    working_dir = joinPath(splitPath(run_rpc_api_tests_path)[:-1])
#    os.chdir(working_dir)
#    for method_type in getDecoratorsDict().keys():
#      for method_name in tested_instance.exposedMethods(method_type):
#        cmd = 'node %s %s %s' % (run_rpc_api_tests_path, javascript_test_path, method_name)
#        stdout, stderr = command_runner.run(cmd)
#        self.log('Javascript stdout: """%s"""' % stdout)
#        self.log('Javascript stderr: """%s"""' % stderr)
#
#  def runAllTests(self, package):
#    pass
#
#  def __getSortedNames(self, tests_dict):
#    return sorted([module.__name__ for module in tests_dict.keys()])
#
#  def printTestsNumbers(self, package):
#    tests_dict = self._getTestDict(package)
#    sorted_names = self.__getSortedNames(tests_dict)
#    self.log.i('Test N| Test Name')
#    for index, name in enumerate(sorted_names):
#      self.log.i('% 6d\t%s' % (index, name))

#  def _getTestDict(self, package):
#    tests_dict = PackageClassesInspector(self.context).buildModulesDict(package, DRModuleUnitTestBase)
#    return tests_dict

def smokeTestModule():
  from simplerpc.context.SimpleRpcContext import SimpleRpcContext
  context = SimpleRpcContext('smoke test')
  mutr = ModuleUnitTestRunner(context)
  from example_rpc.exposed_api.images.ImagesBrowser \
  import ImagesBrowser as tested_class
  from example_rpc.tests.twin_unittests.exposed_api.images.ImagesBrowser \
  import ImagesBrowser as tester_class
  mutr.runSingleTest(tester_class, tested_class)

if __name__ == "__main__":
  smokeTestModule()
