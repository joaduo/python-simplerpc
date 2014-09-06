# -*- coding: utf-8 -*-
'''
Simple RPC
Copyright (c) 2012-2013, LastSeal S.A.
'''
from simplerpc.common.abstract.FrameworkBase import FrameworkBase
import os

class SimpleRpcLogicBase(FrameworkBase):
    '''
    #TODO: document
    '''
    def _getProjectPath(self):
        return os.path.dirname(self.context.project_package.__file__)

def smokeTestModule():
    from simplerpc.context.SimpleRpcContext import SimpleRpcContext
    context = SimpleRpcContext('smoke test')
    SimpleRpcLogicBase(context)

if __name__ == "__main__":
    smokeTestModule()
