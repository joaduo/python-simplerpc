# -*- coding: utf-8 -*-
'''
Copyright (c) 2013, LastSeal S.A.
Copyright (c) 2011-2012, Joaquin G. Duo
All rights reserved.

This code is distributed under BSD 3-clause License.
For details check the LICENSE file in the root of the project.
'''
from simplerpc.common.context.ContextWrapper import ContextWrapper
from simplerpc.common.context.base import ContextBase

class ContextClientBase(object):
    '''
      Classes inheriting from 'ContextClientBase' will have easier access to the
      global config embedded in the context object.
      They will do to save some global config:
        self.context.some_parameter = <value>
      And to retrieve it:
        <variable> = self.context.some_parameter
      Without this wrapper the class should have to do:
        <variable> = self.context.get_config(self.__class__,'some_parameter')
      This way, accessing to the global config is straightforward.
    '''
    def __init__(self, context=None):
        self.context = self.__setContext(context)
    def __healthContext(self, context):
        return isinstance(context, ContextWrapper) or isinstance(context, ContextBase)
    def __setContext(self, context):
        if context == None:
            raise TypeError("You should provide a Context for this object since it " \
                               "inherits from %r" % self.__class__)
        elif not self.__healthContext(context):
            raise TypeError('Provided context %r is of incorrect type' % context)
        else:
            #The context need to be wrapped in order to have easier access to the global config
            if not isinstance(context, ContextWrapper):
                context = ContextWrapper(context)
        return context

def smokeTestModule():
    class Context(ContextBase):
        def _loadInitConfig(self):
            pass
    context = Context('smoke test')
    ContextClientBase(context)
    for ctx in [None, list]:
        try:
            ContextClientBase(ctx)
        except TypeError:
            pass

if __name__ == '__main__':
    smokeTestModule()
