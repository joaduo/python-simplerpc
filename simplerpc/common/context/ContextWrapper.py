'''
Copyright (c) 2013, LastSeal S.A.
Copyright (c) 2011-2012, Joaquin G. Duo
All rights reserved.

This code is distributed under BSD 3-clause License. 
For details check the LICENSE file in the root of the project.
'''


#TODO: rename to ConfigWrapper
class ContextWrapper(object):
  '''
    Provides a wrapper for a context object.
    This wrapper is used by other classes for managing the global config.
    ContextClientBase    
    They will do to save some config:
      self.context.config.some_parameter = <value>
      self.context.some_parameter = <value>
    And to retrieve it:
      <variable> = self.context.config.some_parameter
    Where 'self' would be an instance of this class.
    Without this wrapper the class should have to do:
      <variable> = self.context.get_config('global','some_parameter')
    This way, accessing to the global config is straightforward. 
  '''
  def __init__(self,context):
    object.__setattr__(self,'context', context)
    object.__setattr__(self,'name', context.name)
  def __getattr__(self, name):
    if name in ['context','name']:
      object.__getattribute__(self,name)
    elif name in ['config']:
      return self
    elif name in ['has_config','get_config','set_config']:
      return getattr(self.context, name)
    elif self.context.has_config(name):
      return self.context.get_config(name)
    else:
      raise AttributeError('There is no global config for %r ' % (name))
  def __setattr__(self, name,value):
    reserved = ['has_config', 'get_config', 'set_config']
    if name not in reserved:
      self.context.set_config(name, value)
    else:
      AttributeError('Attribute name %r is in reserved names %r ' % (name, reserved))

def smokeTestModule():
  from simplerpc.common.context.base import ContextBase
  class Context(ContextBase):
    def _loadInitConfig(self):
      pass

  ctx = ContextWrapper(Context('smoke test'))
  ctx.foo = 'bar'
  assert ctx.foo == 'bar'
  try:
    ctx.bar
  except AttributeError:
    pass

  try:
    ctx.has_config = None
  except AttributeError:
    pass

if __name__ == '__main__':
  smokeTestModule()
