# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.base.SimpleRpcLogicBase import SimpleRpcLogicBase
from simplerpc.expose_api.javascript.ClassToJs import ClassToJs
from simplerpc.expose_api.javascript.data_model import AutoTemplateAstNode
from simplerpc.context.SimpleRpcContext import SimpleRpcContext
from simplerpc.expose_api.ExposedPackageBrowser import ExposedPackageBrowser

class PackageToJs(SimpleRpcLogicBase):
    '''
    Translates a package into Javascript to expose classes inside that package
    '''
    def __post_init__(self):
        self.package_browser = ExposedPackageBrowser(self.context)

    def translatePackage(self, package, class_translator=None):
        if not class_translator:
            class_translator = ClassToJs(self.context)
        classes_node = AutoTemplateAstNode()
        for class_ in self.package_browser.getExposedClasses(package):
            n = class_translator.translateClass(class_)
            classes_node.translate(class_.__name__, n)
        return classes_node

def smokeTestModule():
    context = SimpleRpcContext('smoke test')
    import example_rpc.exposed_api.images as images
    tree = PackageToJs(context).translatePackage(images)
    context.log(tree)
    from simplerpc.expose_api.javascript.TemplatesCollector import TemplatesCollector
    templates = TemplatesCollector(context).collectBuiltIn()
    context.log(tree.getString(templates))

if __name__ == "__main__":
    smokeTestModule()
