# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from unittest.case import TestCase
from simplerpc.testing.exposed_api.TwinModulesManager import TwinModulesManager
from simplerpc.context.SimpleRpcContext import SimpleRpcContext
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.common.FileManager import FileManager
from simplerpc.testing.exposed_api.ModuleUnitTestRunner import ModuleUnitTestRunner

class ExposedTestBase(SimpleRpcLogicBase):
    tests_context = None

    @staticmethod
    def setTestsContext(context):
        ExposedTestBase.tests_context = context

    def __init__(self, first_arg=None):
        #Initialize the class if inheriting from TestCase
        if isinstance(self, TestCase): #If using unittest, then initialize the class
            #Keep signature
            if isinstance(first_arg, str):
                methodName = first_arg
                first_arg = None
                TestCase.__init__(self, methodName)
            else:
                TestCase.__init__(self)

        context = first_arg
        #Solve context if not provided
        if context == None:
            if ExposedTestBase.tests_context == None: #To enable context free initialization supporting unittest.TestCase
                self.__runs_from_tested_module = False
                ExposedTestBase.tests_context = SimpleRpcContext(self.__class__.__name__)
            else:
                self.__runs_from_tested_module = True
            context = ExposedTestBase.tests_context
        SimpleRpcLogicBase.__init__(self, context)

    def __post_init__(self):
        self.twins_manager = TwinModulesManager(self.context)
        self.module_unit_test_runner = ModuleUnitTestRunner(self.context)
        self.file_manager = FileManager(self.context)

    def runTest(self):
        pass

    def __printTestedClassFile(self, tested_class):
        path = self.file_manager.formatClassFilePath(tested_class)
        name = tested_class.__name__
        self.log.d('Testing %r at:\n %s' % (name, path))

    def testJsJasmine(self):
        tested_class = self._getTestedClass()
        self.module_unit_test_runner.runJsTest(tested_class)

    def testMethodsExistence(self):
        tested_class = self._getTestedClass()
        if not self.__runs_from_tested_module:
            self.__printTestedClassFile(tested_class)
        #tested_instance =
        for name, attrib in tested_class.__dict__.items():
            if callable(attrib) and not name.startswith('_'):
                test_name = 'test_%s' % name
                msg = 'There is no test test_%s for class %r' % (name, tested_class)
                assert test_name in self.__class__.__dict__, msg
                #assert callable(self.__class__.__dict__[test_name]) #TODO: necessary?

    def _getTestedClass(self):
        return self.twins_manager.getTestedFromTester(self.__class__)

def smokeTestModule():
    context = SimpleRpcContext('smoke test')
    ExposedTestBase(context)#.runTest()

if __name__ == "__main__":
    smokeTestModule()
