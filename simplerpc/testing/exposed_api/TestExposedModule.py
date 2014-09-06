# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.testing.exposed_api.ModuleUnitTestRunner import ModuleUnitTestRunner
from simplerpc.expose_api.base.ExposedBase import ExposedBase
from importlib import import_module
import os
from simplerpc.SimpleRpcError import SimpleRpcError
from inspect import isclass

class TestExposedModule(SimpleRpcLogicBase):
    '''
    Class to test an exposed module given its file path.
    Will run the python and javascript unittests.
    '''
    def __post_init__(self):
        self.module_unittest_runner = ModuleUnitTestRunner(self.context)

    def __getModuleName(self, file_path):
        file_path = os.path.realpath(os.path.splitext(file_path)[0])
        name = None
        for package in self.context.exposed_roots:
            prefix = os.path.realpath(package.__path__[0])
            if os.path.commonprefix((prefix, file_path)) == prefix:
                name = os.path.relpath(file_path, prefix)
                break
        if name == None:
            msg = 'Cannot find module for exposed module %r' % file_path
            raise SimpleRpcError(msg)
        name = package.__name__ + '.' + '.'.join(os.path.split(name))
        return name

    def __getTestedClass(self, module):
        for attr in module.__dict__.values():
            if isclass(attr) and issubclass(attr, ExposedBase) \
              and attr.__module__ == module.__name__:
                return attr
        raise SimpleRpcError('Cannot find exposed class in %r' % module)

    def testModule(self, file_path):
        name = self.__getModuleName(file_path)
        module = import_module(name)
        tested_class = self.__getTestedClass(module)
        self.module_unittest_runner.runPythonTest(tested_class)

def smokeTestModule():
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    from simplerpc.common.path import joinPath
    context = SimpleRpcContext('test exposed')
    tec = TestExposedModule(context)
    file_path = joinPath(tec._getProjectPath(), 'exposed_api/images/ImagesBrowser.py')
    tec.testModule(file_path)

if __name__ == "__main__":
    smokeTestModule()
