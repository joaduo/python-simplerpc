# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.testing.exposed_api.TwinModulesManager import TwinModulesManager
from simplerpc.testing.exposed_api.ModuleUnitTestRunner import ModuleUnitTestRunner
from simplerpc.context.SimpleRpcContext import SimpleRpcContext
from simplerpc.common.FileManager import FileManager
from simplerpc.expose_api.javascript.ClassToJsUnitTest import ClassToJsUnitTest
import os
import logging

class ExposedModuleAutotester(SimpleRpcLogicBase):
    '''
    #TODO: document
    '''
    def __init__(self, context=None):
        if context == None:
            context = SimpleRpcContext(self.__class__.__name__)
            context.log.setLevel(logging.DEBUG)
        SimpleRpcLogicBase.__init__(self, context)

    def __post_init__(self):
        self.twins_manager = TwinModulesManager(self.context)
        self.module_unit_test_runner = ModuleUnitTestRunner(self.context)
        self.file_manager = FileManager(self.context)
        self.class_to_js_unittest = ClassToJsUnitTest(self.context)

    def autoTest(self):
        tested_class = self.__getTestedClass()
        self.module_unit_test_runner.runPythonTest(tested_class)

    def createJsUnitTest(self, overwrite=False):
        tested_class = self.__getTestedClass()
        file_path = self.twins_manager.getJsUnittest(tested_class)
        self.class_to_js_unittest.translateToFile(tested_class, file_path, overwrite)

    def __getClassName(self, module_path):
        return os.path.splitext(os.path.basename(module_path))[0]

    def __getTestedClass(self):
        import __main__
        return getattr(__main__, self.__getClassName(__main__.__file__))


def smokeTestModule():
    context = SimpleRpcContext('smoke test')
    ema = ExposedModuleAutotester(context)
    def getTestedClass():
        from example_rpc.exposed_api.images.ImagesBrowser import ImagesBrowser
        return ImagesBrowser
    ema._ExposedModuleAutotester__getTestedClass = getTestedClass
    ema.autoTest()
    ema.createJsUnitTest(overwrite=False)

if __name__ == "__main__":
    smokeTestModule()
