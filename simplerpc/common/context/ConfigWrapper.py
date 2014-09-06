'''
Copyright (c) 2013, LastSeal S.A.
Copyright (c) 2011-2012, Joaquin G. Duo
All rights reserved.

This code is distributed under BSD 3-clause License.
For details check the LICENSE file in the root of the project.
'''

class NoConfigError(RuntimeError):
    pass

#TODO: rename to ContextClassConfigWrapper
class ConfigWrapper(object):
    '''
      Provides a wrapper for a context object to have easier access to a
      class' own config.
      This wrapper is used by classes inheriting from 'SelfConfigBase'
      for reading and writing its own config.
    '''
    def __init__(self, owner_class, context):
        object.__setattr__(self, 'owner_class', owner_class)
        object.__setattr__(self, 'context', context)
    def __getattr__(self, name):
        #TODO:CODE VALIDATION validate call stack
        if name in ['context', 'owner_class']: #context and owner_class shouldn't be intercepted
            object.__getattribute__(self, name)
        elif self.context.has_config(name, self.owner_class): #Intercept other config name
            return self.context.get_config(name, self.owner_class)
        else: #there is no config for such name
            raise NoConfigError('There is no config for %r of the class %r' %
                                (name, self.owner_class))
    def has(self, name):
        try:
            self.__getattr__(name)
            return True
        except NoConfigError:
            return False
    def __setattr__(self, name, value):
        key_names = ['context', 'owner_class']
        if name not in key_names : #context and owner_class shouldn't be intercepted
            self.context.set_config(name, value, self.owner_class)
        else:
            class_str = "%s.%s" % (self.owner_class.__module__.__str__(), self.owner_class.__name__)
            raise AttributeError('You shouldn\'t reserverd attributes in %r for a '
                                 'class\' own config. (%r in this case) \n' % \
                                 (key_names, class_str))


def smokeTestModule():
    from simplerpc.common.context.base import ContextBase
    from simplerpc.common.context.ContextWrapper import ContextWrapper
    class Context(ContextBase):
        def _loadInitConfig(self):
            pass
    ctx = ContextWrapper(Context('smoke test'))
    class Example(object):
        pass
    config = ConfigWrapper(Example, ctx)
    config.foo = 'bar'
    assert config.foo == 'bar'
    try:
        config.bar
    except NoConfigError as e:
        pass

if __name__ == '__main__':
    smokeTestModule()
