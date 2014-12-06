# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.common.PackageClassesInspector import ModulesAttributesIterator
from unittest.loader import TestLoader
from unittest.case import TestCase
from unittest.runner import TextTestRunner
from unittest.suite import TestSuite
from types import FunctionType


class SmokeTestRunner(SimpleRpcLogicBase):
    '''
    Inspect in all simplerpc modules for a smokeTestModule function.
    Then create a test for each class and runs it.
    '''
    def __post_init__(self):
        self.inspector = ModulesAttributesIterator(self.context)

    def __gatherTests(self, package):
        filter_func = lambda attr, module: callable(attr) \
                                          and hasattr(attr, '__name__') \
                                          and attr.__name__ == 'smokeTestModule'
        func_dict = self.inspector.buildDict(package, filter_func, reload_=False)
        new_dict = {}
        for module, funcs in func_dict.items():
            if len(funcs):
                new_dict[module] = funcs[0]
        return new_dict

    def getModulesWithoutTests(self):
        package = self.__getPackage()
        filter_func = lambda attr, module: isinstance(attr, FunctionType)
        func_dict = self.inspector.buildDict(package, filter_func, reload_=False)
        missing = []
        for module, funcs in func_dict.items():
            has_test = filter(lambda x: x.__name__ == 'smokeTestModule', funcs)
            #smokeTest exists, or is not this module
            if (not len(has_test) or not len(funcs)) \
              and not module.__name__.split('.')[-1] == self.__class__.__name__:
                missing.append(module)
        return missing

    def __getPackage(self):
        import simplerpc
        return simplerpc

    def runTests(self):
        func_dict = self.__gatherTests(self.__getPackage())
        self.__runFunctions(func_dict)

    def __createTestClass(self, func):
        log = self.context.log
        class SmokeTest(TestCase):
            def testSmokeTest(self):
                log('Testing %s' % func.__module__)
                func()
        return SmokeTest

    def __runFunctions(self, func_dict):
        suites = []
        for _, func in func_dict.items():
            s = TestLoader().loadTestsFromTestCase(self.__createTestClass(func))
            suites.append(s)
        big_suite = TestSuite(suites)
        TextTestRunner().run(big_suite)

def run():
    from simplerpc.common.path import formatPathPrint
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    from simplerpc.common.log.Logger import Logger
    import simplerpc.common.log.printSmoke as printSmoke
    import logging
    printSmoke.do_print = False
    Logger.default_level = logging.ERROR
    Logger.handler_level = logging.ERROR
    context = SimpleRpcContext('smoke test')
    s = SmokeTestRunner(context)
    s.runTests()
    for m in s.getModulesWithoutTests():
        f = m.__file__
        if f.endswith('.pyc'):
            f = f[:-1]
        context.log('Missing test in module %s' % m)
        context.log(formatPathPrint(f))

if __name__ == "__main__":
    run()
