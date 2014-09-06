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
from simplerpc.testing.exposed_api.TwinModulesManager import TwinModulesManager
from simplerpc.common.FileManager import FileManager
from simplerpc.expose_api.javascript.NodeJsRunner import NodeJsRunner
from simplerpc.SimpleRpcError import SimpleRpcError
#import os

class ModuleUnitTestRunner(SimpleRpcLogicBase):
    def __post_init__(self):
        self.twins_manager = TwinModulesManager(self.context)
        self.file_manager = FileManager(self.context)
        self.nodejs = NodeJsRunner(self.context)

    def runTestByNumber(self, package, test_number):
        tests_dict = self._getTestDict()
        sorted_names = self.__getSortedNames(tests_dict)
        new_dict = dict((module.__name__, class_) for module, class_ in tests_dict.items())
        tester_class = new_dict[sorted_names[test_number]]
        self.runPythonTest(tester_class)

    def __runUnitTest(self, tester_class):
        tester_class.setTestsContext(self.context)
        suite = TestLoader().loadTestsFromTestCase(tester_class)
        TextTestRunner().run(suite)

    def runPythonTest(self, tested_class):
        tester_class = self.twins_manager.getTesterFromTested(tested_class)
        path = self.file_manager.formatClassFilePath(tester_class)
        name = tester_class.__name__
        self.log.d('Running %r test at:\n %s' % (name, path))
        #self.module_unit_test_runner.runPythonTest(tester_class)
        self.__runUnitTest(tester_class)

    def runJsTest(self, tested_class):
        file_path = self.twins_manager.getJsUnittest(tested_class)
        path = self.file_manager.formatFilePath(file_path)
        self.log.d('Running jasmine test at:\n%s' % path)
        ret_val = self.nodejs.runJasmineTest(file_path)
        if ret_val:
            raise SimpleRpcError('Jasmine test failed')

def smokeTestModule():
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    context = SimpleRpcContext('smoke test')
    mutr = ModuleUnitTestRunner(context)
    from example_rpc.exposed_api.images.ImagesBrowser \
    import ImagesBrowser as tested_class
    mutr.runPythonTest(tested_class)

if __name__ == "__main__":
    smokeTestModule()
