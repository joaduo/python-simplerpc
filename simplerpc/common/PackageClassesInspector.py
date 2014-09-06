# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from importlib import import_module
import pkgutil

class ModulesAttributesIterator(SimpleRpcLogicBase):
    def getChildModules(self, package, reload_=False):
        return self._gatherModules(package, reload_)

    def buildDict(self, package, filter_func, reload_=False):
        modules = self._gatherModules(package, reload_)
        modules_dict = {}
        for module in modules:
            filtered = self._filterModule(module, filter_func)
            modules_dict[module] = filtered
        return modules_dict

    def _filterModule(self, module, filter_func):
        classes = []
        for attr in module.__dict__.values():
            if filter_func(attr, module):
                classes.append(attr)
        return classes

    def _gatherModules(self, package, reload_):
        modules = []
        prefix = package.__name__ + '.'
        for _, modname, ispkg in pkgutil.walk_packages(package.__path__, prefix):
            if not ispkg:
                module = import_module(modname)
                if reload_:
                    module = reload(module)
                modules.append(module)
        return modules

def smokeTestModule():
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    context = SimpleRpcContext('smoke test')
    mai = ModulesAttributesIterator(context)
    import example_rpc.exposed_api as package
    context.log(mai.getChildModules(package))
    from inspect import isclass
    filter_func = lambda attr, module: isclass(attr)
    context.log(mai.buildDict(package, filter_func))

if __name__ == "__main__":
    smokeTestModule()
