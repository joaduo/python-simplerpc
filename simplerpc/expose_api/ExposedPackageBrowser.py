# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2013, Joaquin G. Duo
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from inspect import isclass
from simplerpc.expose_api.base.ExposedBase import ExposedBase
from simplerpc.common.PackageClassesInspector import ModulesAttributesIterator

class ExposedPackageBrowser(SimpleRpcLogicBase):
    '''
    #TODO: document
    '''
    def __post_init__(self):
        self.modules_inspector = ModulesAttributesIterator(self.context)

    def __buildDict(self, package, filter_func, reload_=True):
        return self.modules_inspector.buildDict(package, filter_func, reload_)

    def getExposedClasses(self, package):
        filter_func = lambda attr, module: isclass(attr) \
                                            and issubclass(attr, ExposedBase) \
                                            and attr.__module__ == module.__name__
        classes = self.__buildDict(package, filter_func).values()
        classes = [c[0] for c in classes if len(c)]
        return classes

    def getModuleAndClass(self, package):
        filter_func = lambda attr, module: isclass(attr) \
                                            and issubclass(attr, ExposedBase) \
                                            and attr.__module__ == module.__name__
        classes = self.__buildDict(package, filter_func)
        classes = [(m, c[0]) for m, c in classes.items() if len(c)]
        return classes

def smokeTestModule():
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    context = SimpleRpcContext('smoke test')
    import example_rpc.exposed_api as exposed_api
    context.log(ExposedPackageBrowser(context).getExposedClasses(exposed_api))

if __name__ == "__main__":
    smokeTestModule()
